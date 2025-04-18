import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT")) 

# Connect to MySQL
def connect():
    global connection, cursor
    connection = mysql.connector.connect(
        host=MYSQLHOST,
        user=MYSQLUSER,
        password=MYSQLPASSWORD,
        port=MYSQLPORT 
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
create_table_query_goal = """ 
CREATE TABLE IF NOT EXISTS goal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    goal DECIMAL(10,2) DEFAULT 0.00,
    goal_gross DECIMAL(10,2) DEFAULT 0.00,
    goal_start DATE NOT NULL,
    goal_end DATE NOT NULL,
    day_off INT DEFAULT 0,
    fleet_discount DECIMAL(5,2) DEFAULT 0.00,
    tax_discount DECIMAL(5,2) DEFAULT 0.00,
    total_gain DECIMAL(10,2) DEFAULT 0.00,
    goal_successful VARCHAR(20) DEFAULT 'negativo',
    UNIQUE(user_id, goal_start, goal_end),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

create_table_query_uber = """ 
CREATE TABLE IF NOT EXISTS uber (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    daily_value DECIMAL(10, 2) NOT NULL,
    daily_value_tips DECIMAL(10, 2) NOT NULL,
    daily_date DATE NOT NULL,
    working_hours VARCHAR(50),
    distance_traveled DECIMAL(10, 2),
    trips_made INT,
    observation TEXT,
    daily_reimbursement DECIMAL(10, 2),
    UNIQUE(user_id, daily_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

create_table_query_bolt = """ 
CREATE TABLE IF NOT EXISTS bolt (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    daily_value DECIMAL(10, 2) NOT NULL,
    daily_value_tips DECIMAL(10, 2),
    daily_date DATE NOT NULL,
    working_hours VARCHAR(50),
    distance_traveled DECIMAL(10, 2),
    trips_made INT,
    observation TEXT,
    daily_reimbursement DECIMAL(10, 2),
    UNIQUE(user_id, daily_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

create_table_query_expense = """ 
CREATE TABLE IF NOT EXISTS expense (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    expense_value DECIMAL(10, 2) NOT NULL,
    expense_date DATE NOT NULL,
    expense_name VARCHAR(100) NOT NULL,
    expense_amount_liters DECIMAL(10, 2),
    expense_amount_energy DECIMAL(10, 2),
    expense_amount_cubic_meters DECIMAL(10, 2),
    observation_expense TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

"""

cursor.execute(create_table_query)
cursor.execute(create_table_query_goal)
cursor.execute(create_table_query_uber)
cursor.execute(create_table_query_bolt)
cursor.execute(create_table_query_expense)

   # Commit the transactio

commit_and_close_db()

print("Database and table created successfully.", )

#connect()

