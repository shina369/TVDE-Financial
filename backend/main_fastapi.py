from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel
import mysql.connector
import logging
import sys
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

logger = logging.getLogger("upgrade_service")
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# =========================
# Variáveis de ambiente
# =========================
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT") or 3306)

PLAY_PACKAGE_NAME = os.getenv("PLAY_PACKAGE_NAME")
PLAY_PRODUCT_ID = os.getenv("PLAY_PRODUCT_ID")

# =========================
# Função para inicializar Google Play API
# =========================
def get_play_service():
    try:
        service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/androidpublisher"]
        )
        return build("androidpublisher", "v3", credentials=credentials, cache_discovery=False)
    except Exception as e:
        logger.error(f"Erro ao inicializar Google Play API: {e}")
        raise HTTPException(status_code=500, detail="Erro ao inicializar Google Play API")


# =========================
# FastAPI app
# ========================

# ----------------------------
# Teste básico
# ----------------------------
@app.get("/")
def root():
    return {"status": "FastAPI rodando no Railway"}


# ----------------------------
# Banco temporário em memória
# ----------------------------
logged_emails = {}  # session_id -> email


@app.post("/set_logged_email_simple")
def set_logged_email_simple(data: dict = Body(...)):
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email não fornecido")

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=MYSQLHOST,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database="db_tvde_users_external",
            port=MYSQLPORT
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return {"status": "success", "email": email}

    except HTTPException:
        raise
    except Exception as e:
        logger.info(f"Erro em set_logged_email_simple: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# =========================
# Modelo de requisição
# =========================
class UpgradeRequest(BaseModel):
    email: str
    purchaseToken: str


class UpdateAccountRequest(BaseModel):
    email: str
    account_type: str


# =========================
# Endpoint /upgrade
# =========================
@app.post("/upgrade")
def upgrade(req: UpgradeRequest):
    if req.email not in logged_emails:
        raise HTTPException(status_code=401, detail="Email não registrado no login")

    # Inicializa o serviço da Google Play sob demanda
    play_service = get_play_service()

    try:
        result = play_service.purchases().products().get(
            packageName=PLAY_PACKAGE_NAME,
            productId=PLAY_PRODUCT_ID,
            token=req.purchaseToken
        ).execute()
        logger.info(f"Resultado do token: {result}")
    except Exception as e:
        logger.info(f"Erro ao validar token: {e}")
        raise HTTPException(status_code=400, detail="Erro ao validar token na Google Play")

    if result.get("purchaseState") != 0:
        logger.info(f"Compra inválida ou não concluída para token {req.purchaseToken}")
        raise HTTPException(status_code=400, detail="Compra inválida ou não concluída")

    conn, cursor = None, None
    try:
        conn = mysql.connector.connect(
            host=MYSQLHOST,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database="db_tvde_users_external",
            port=MYSQLPORT
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, account_type FROM users WHERE email = %s", (req.email,))
        user = cursor.fetchone()

        if not user:
            logger.info(f"Usuário não encontrado: {req.email}")
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        account_type_value = str(user.get("account_type", "")).lower() if isinstance(user, dict) else str(user[1]).lower()

        if account_type_value == "premium":
            return {"status": "success", "account_type": "Premium", "message": "Usuário já é Premium"}

        cursor.execute(
            "UPDATE users SET account_type = %s WHERE email = %s",
            ("Premium", req.email)
        )
        conn.commit()
        logger.info(f"Usuário {req.email} atualizado para Premium")

    except HTTPException:
        raise
    except Exception as e:
        logger.info(f"Erro ao atualizar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return {"status": "success", "account_type": "Premium", "message": "Usuário atualizado para Premium"}


@app.get("/user_status")
def get_status_usuario(email: str):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=MYSQLHOST,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database="db_tvde_users_external",
            port=MYSQLPORT
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT account_type FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            return {"account_type": "Básico"}
        return {"account_type": user["account_type"]} if isinstance(user, dict) else {"account_type": user[0]}
    except Exception as e:
        logger.info(f"Erro ao buscar status do usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
