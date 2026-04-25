import sqlite3

conn = sqlite3.connect("database/escola.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE aulas ADD COLUMN compareceu INTEGER DEFAULT 0")
except:
    pass

try:
    cursor.execute("ALTER TABLE aulas ADD COLUMN nota REAL")
except:
    pass

conn.commit()
conn.close()

print("Banco atualizado com sucesso!")