import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""  
)

cursor = connection.cursor()

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

# Commit the transaction
connection.commit()

# Close the connection
cursor.close()
connection.close()

print("Database and table created successfully.", )