import sqlite3

# Conectar ao SQLite
def connect():
    global connection, cursor
    # Conecta ou cria o banco de dados SQLite
    connection = sqlite3.connect('db_tvde_content_internal.db')
    cursor = connection.cursor()
    print("Conectado com sucesso ao banco de dados SQLite!")

# Salvar e fechar a conexão
def commit_and_close_db():
    connection.commit()
    cursor.close()
    connection.close()
    print("Conexão com o banco de dados fechada com sucesso.")

# Conectar ao banco de dados
connect()

# Criar a tabela goal
create_table_query = """
CREATE TABLE IF NOT EXISTS goal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT NOT NULL,
    goal_start TEXT NOT NULL,
    goal_end TEXT NOT NULL,
    day_off TEXT NOT NULL,
    fleet_discount TEXT NOT NULL,
    tax_discount TEXT NOT NULL
);
"""
create_table_query_bolt = """
CREATE TABLE IF NOT EXISTS bolt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bolt_daily_value TEXT NOT NULL,
    bolt_tips TEXT NOT NULL,
    bolt_daily_date TEXT NOT NULL,
    bolt_time_run TEXT NOT NULL,
    bolt_distance_run TEXT NOT NULL,
    bolt_trip TEXT NOT NULL,
    bolt_observation TEXT NOT NULL
);
"""

create_table_query_uber = """
CREATE TABLE IF NOT EXISTS uber (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uber_daily_value TEXT NOT NULL,
    uber_tips TEXT NOT NULL,
    uber_daily_date TEXT NOT NULL,
    uber_time_run TEXT NOT NULL,
    uber_distance_run TEXT NOT NULL,
    uber_trip TEXT NOT NULL,
    uber_observation TEXT NOT NULL
);
"""
create_table_query_expense = """
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_value TEXT NOT NULL,
    expense_date TEXT NOT NULL,
    expense_name TEXT NOT NULL,
    expense_amount TEXT NOT NULL,
    expense_observation TEXT NOT NULL
);
"""

cursor.execute(create_table_query)
cursor.execute(create_table_query_bolt)
cursor.execute(create_table_query_uber)
cursor.execute(create_table_query_expense)

# Salvar a transação e fechar o banco de dados
commit_and_close_db()

print("Database and table created successfully.")
