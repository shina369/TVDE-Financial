from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import logging
import sys
import os
import json
from dotenv import load_dotenv
from fastapi import Body

load_dotenv()

logger = logging.getLogger("upgrade_service")
logger.setLevel(logging.INFO)

# Remove handlers antigos, se existirem
if logger.hasHandlers():
    logger.handlers.clear()

# Cria um handler para enviar logs para stdout
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# =========================
# Variáveis de ambiente e Google Play
# =========================
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT") or 3306)

PLAY_PACKAGE_NAME = os.getenv("PLAY_PACKAGE_NAME")
PLAY_PRODUCT_ID = os.getenv("PLAY_PRODUCT_ID")

service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/androidpublisher"]
)
play_service = build("androidpublisher", "v3", credentials=credentials, cache_discovery=False)

# =========================
# FastAPI app
# =========================
app = FastAPI()

from fastapi import Query

# ----------------------------
# Banco temporário em memória
# ----------------------------
logged_emails = {}  # session_id -> email

@app.post("/set_logged_email_simple")
def set_logged_email_simple(data: dict = Body(...)):
    """
    Recebe apenas o email do usuário logado e valida no MySQL.
    """
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

# =========================
# Modelo de requisição para /update_account
# =========================
class UpdateAccountRequest(BaseModel):
    email: str
    account_type: str


# =========================
# Endpoint /upgrade
# =========================
@app.post("/upgrade")
def upgrade(req: UpgradeRequest):
    """
    Recebe email + purchaseToken do app Flutter,
    valida token na Google Play e, se OK,
    atualiza o account_type do usuário para 'Premium'.
    Só aceita se o email já foi registrado em /set_logged_email_simple.
    """
    # ====== Checar se email foi registrado no login ======
    if req.email not in logged_emails:
        raise HTTPException(status_code=401, detail="Email não registrado no login")

    # ====== Validação do token ======
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

    # purchaseState == 0 → compra concluída
    if result.get("purchaseState") != 0:
        logger.info(f"Compra inválida ou não concluída para token {req.purchaseToken}")
        raise HTTPException(status_code=400, detail="Compra inválida ou não concluída")

    # ====== Atualizar usuário no MySQL ======
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

        if isinstance(user, dict):
            account_type_value = str(user.get("account_type", "")).lower()
        else:
            account_type_value = str(user[1]).lower()  # porque SELECT trouxe 2 colunas (id, account_type)

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
        # Ensure user is a dictionary before accessing key
        if isinstance(user, dict):
            return {"account_type": user["account_type"]}
        else:
            # If user is a tuple, get the first element
            return {"account_type": user[0]}
    except Exception as e:
        logger.info(f"Erro ao buscar status do usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
