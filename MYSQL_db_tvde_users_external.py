import mysql.connector
import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

# Obter os dados do ambiente
MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT", 3306))  # Garantir que a porta seja um inteiro

# Conectar ao MySQL
def connect():
    global connection, cursor
    connection = mysql.connector.connect(
        host=MYSQLHOST,
        user=MYSQLUSER,
        password=MYSQLPASSWORD,
        database=MYSQL_DATABASE,  # Conectar diretamente ao banco de dados
        port=MYSQLPORT  # Usar a porta configurada
    )

    cursor = connection.cursor()
    if connection.is_connected():
        print("✅ Conectado ao banco de dados com sucesso!")

# Commit e fechamento da conexão
def commit_and_close_db():
    connection.commit()
    cursor.close()
    connection.close()
    if not connection.is_connected():
        print("❌ Conexão com o banco de dados fechada com sucesso.")

# Conectar e criar banco de dados
connect()

# Criar banco de dados se não existir
cursor.execute("CREATE DATABASE IF NOT EXISTS db_tvde_users_external")

# Usar o banco de dados criado
cursor.execute("USE db_tvde_users_external")

# Criar a tabela de usuários
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    account_type VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    date_start VARCHAR(255) NOT NULL
)
"""
cursor.execute(create_table_query)

# Commit e fechamento
commit_and_close_db()

print("✅ Banco de dados e tabela criados com sucesso.")
