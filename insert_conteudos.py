import sqlite3

conn = sqlite3.connect("database/escola.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO conteudos (titulo, descricao) VALUES ('Matemática','Aulas de matemática')")
cursor.execute("INSERT INTO conteudos (titulo, descricao) VALUES ('Português','Aulas de português')")
cursor.execute("INSERT INTO conteudos (titulo, descricao) VALUES ('Inglês','Aulas de inglês')")

conn.commit()
conn.close()

print("Conteúdos inseridos!")