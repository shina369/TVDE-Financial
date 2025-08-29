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
@app.post("/upgrade_test")
def upgrade_test(req: UpgradeRequest, test_mode: Optional[bool] = True):
    """
    Endpoint de teste: atualiza usuário para Premium sem validar token.
    Apenas para testes de backend.
    """
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
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        cursor.execute("UPDATE users SET account_type = %s WHERE email = %s", ("Premium", req.email))
        conn.commit()
        return {"status": "success", "account_type": "Premium", "message": "Usuário atualizado para Premium (modo teste)"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


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
        logger.error(f"Erro ao buscar status do usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
