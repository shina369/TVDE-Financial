from mysql.connector import Error
from dotenv import load_dotenv
import os

import mysql.connector

load_dotenv()

MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT") or 3306)

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=MYSQLHOST,          # Your database host
            database="db_tvde_users_external",        # Your database name
            user=MYSQLUSER,              # Your database username
            password=MYSQLPASSWORD   # Your database password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()

# Example function to execute queries
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        return cursor
    except Error as e:
        print(f"Error executing query: {e}")
        return None