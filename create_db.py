import sqlite3

conn = sqlite3.connect("database/escola.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT,
email TEXT,
telefone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS conteudos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
titulo TEXT,
descricao TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS aulas (
id INTEGER PRIMARY KEY AUTOINCREMENT,
aluno_id INTEGER,
conteudo_id INTEGER,
data TEXT,
horario TEXT,
observacoes TEXT
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso")