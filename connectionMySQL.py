from mysql.connector import pooling, Error
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT") or 3306)

# Cria o pool de conexões (feito uma única vez)
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="tvde_pool",
        pool_size=5,  # número de conexões que ficarão abertas no pool
        pool_reset_session=True,
        host=MYSQLHOST,
        database=MYSQL_DATABASE,
        user=MYSQLUSER,
        password=MYSQLPASSWORD,
        port=MYSQLPORT
    )
    print(" Pool de conexões MySQL criado com sucesso.")
except Error as e:
    print(f" Erro ao criar pool de conexões: {e}")
    connection_pool = None


def connect_to_database():
    """Obtém uma conexão ativa do pool."""
    if not connection_pool:
        print(" Pool de conexões não inicializado.")
        return None
    try:
        return connection_pool.get_connection()
    except Error as e:
        print(f" Erro ao obter conexão do pool: {e}")
        return None


def close_connection(connection):
    """Devolve a conexão ao pool."""
    if connection and connection.is_connected():
        connection.close()  # devolve ao pool (não destrói realmente)


def execute_query(connection, query, params=None, fetch_one=False, fetch_all=False):
    """
    Executa uma query SQL (SELECT, INSERT, UPDATE, DELETE).
    - params: tupla com parâmetros (%s)
    - fetch_one: retorna uma linha
    - fetch_all: retorna todas as linhas
    """
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = None

        return result
    except Error as e:
        print(f" Erro ao executar query: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
