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
cursor.execute(create_table_query)

# Salvar a transação e fechar o banco de dados
commit_and_close_db()

print("Database and table created successfully.")
