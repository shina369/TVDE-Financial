import sqlite3
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do MySQL via .env
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT"))

# Obtém o ID do usuário pelo e-mail
def get_user_id_from_mysql(email):
    conn = mysql.connector.connect(
        host=MYSQLHOST,
        user=MYSQLUSER,
        password=MYSQLPASSWORD,
        database="db_tvde_users_external",
        port=MYSQLPORT
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result[0] if result else None

# Cria a pasta onde ficarão os bancos SQLite
os.makedirs("db_usuarios", exist_ok=True)

# Retorna conexão com o banco de dados SQLite do usuário
def get_user_db_connection(user_id):
    db_path = f"db_usuarios/db_user_{user_id}.db"
    return sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)

# Cria as tabelas no banco de dados do usuário
def create_user_tables(user_id):
    with get_user_db_connection(user_id) as conn:
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS goal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            goal_gross REAL NOT NULL,
            goal_start TEXT NOT NULL UNIQUE,
            goal_end TEXT NOT NULL UNIQUE,
            day_off INTEGER NOT NULL,
            fleet_discount REAL NOT NULL,
            tax_discount REAL NOT NULL,
            total_gain REAL,
            goal_successful TEXT DEFAULT 'negativo'
        );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS bolt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_value REAL NOT NULL,
            daily_value_tips REAL,
            daily_date TEXT NOT NULL UNIQUE,
            working_hours TEXT,
            distance_traveled REAL,
            trips_made INTEGER,
            observation TEXT,
            daily_reimbursement REAL
        );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS uber (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_value REAL NOT NULL,
            daily_value_tips REAL NOT NULL,
            daily_date TEXT NOT NULL UNIQUE,
            working_hours TEXT,
            distance_traveled REAL,
            trips_made INTEGER,
            observation TEXT,
            daily_reimbursement REAL
        );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_value REAL NOT NULL,
            expense_date TEXT NOT NULL,
            expense_name TEXT NOT NULL,
            expense_amount_liters REAL,
            expense_amount_energy REAL,
            expense_amount_cubic_meters REAL,
            observation_expense TEXT
        );""")

        print(f"Tabelas criadas para o usuário {user_id}")

# Função principal que integra tudo
def preparar_banco_usuario(email):
    user_id = get_user_id_from_mysql(email)

    if user_id is not None:
        create_user_tables(user_id)
    else:
        print("Usuário não encontrado.")

# ✅ Exemplo de uso no app (após login):
# preparar_banco_usuario(email_do_usuario_logado)
