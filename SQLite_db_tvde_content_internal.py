import sqlite3

# Conectar ao SQLite e criar as tabelas
def connect_and_create_tables():
    with sqlite3.connect('db_tvde_content_internal.db') as connection:
        cursor = connection.cursor()
        
        # Criar a tabela goal
        create_table_query = """
        CREATE TABLE IF NOT EXISTS goal (
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
        );
        """

        create_table_query_bolt = """
        CREATE TABLE IF NOT EXISTS bolt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   
            daily_value REAL NOT NULL,
            daily_value_tips REAL,
            daily_date TEXT NOT NULL UNIQUE,
            working_hours TEXT,
            distance_traveled REAL,
            trips_made INTEGER,
            observation TEXT,
            daily_reimbursement REAL
        );
        """

        create_table_query_uber = """
        CREATE TABLE IF NOT EXISTS uber (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_value REAL NOT NULL,
            daily_value_tips REAL NOT NULL,
            daily_date TEXT NOT NULL UNIQUE,
            working_hours TEXT,
            distance_traveled REAL,
            trips_made INTEGER,
            observation TEXT,
            daily_reimbursement REAL
        );
        """

        create_table_query_expense = """
        CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_value REAL NOT NULL,
            expense_date TEXT NOT NULL,
            expense_name TEXT NOT NULL,
            expense_amount_liters REAL,
            expense_amount_energy REAL,
            expense_amount_cubic_meters REAL,
            observation_expense TEXT
        );
        """

        # Executar a criação das tabelas
        cursor.execute(create_table_query)
        cursor.execute(create_table_query_bolt)
        cursor.execute(create_table_query_uber)
        cursor.execute(create_table_query_expense)

        print("Banco de dados e tabelas criados com sucesso!")

# Criar o banco de dados e tabelas
connect_and_create_tables()
