import mysql.connector

# Connect to MySQL
def connect():
    global connection, cursor
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_tvde_users_external"
        
    )

    cursor = connection.cursor()
def commit_and_close_db():
    connection.commit()
       
    cursor.close()
    connection.close()
def create_data():
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS db_tvde_users_external")

    # Use the new database
    cursor.execute("USE db_tvde_users_external")

    # Create the users table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        user_surname VARCHAR(255) NOT NULL,
        user_email VARCHAR(255) NOT NULL,
        user_password VARCHAR(255) NOT NULL,
        user_profile_photo BLOB
    )
    """
    cursor.execute(create_table_query)

    # Commit the transactio

    print("Database and table created successfully.", )

connect()
create_data()
commit_and_close_db()
