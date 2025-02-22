import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

# Connect to MySQL
def connect():
    global connection, cursor
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))  # Certifique-se de converter a porta para inteiro
    )

    cursor = connection.cursor()
    if connection.is_connected():
        print("Conectado com sucesso!")
# Commit and Close data
def commit_and_close_db():

    connection.commit()
       
    cursor.close()
    connection.close()
    if not connection.is_connected():
        print("Conexão com o banco de dados fechada com sucesso.")

connect()
# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS db_tvde_users_external")

# Use the new database
cursor.execute("USE db_tvde_users_external")

# Create the users table
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

   # Commit the transactio

commit_and_close_db()

print("Database and table created successfully.", )

#connect()

