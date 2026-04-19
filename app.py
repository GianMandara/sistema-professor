from flask import Flask, render_template, request, redirect
import sqlite3
import re
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

EMAIL_REMETENTE = "gianluca.mandara.gm@gmail.com"
SENHA_EMAIL = "knuq zghs pfou quxb"

# =========================
# CONEXÃO
# =========================
def conectar():
    caminho = os.path.join(os.path.dirname(__file__), "database", "escola.db")
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# VALIDAR EMAIL
# =========================
def email_valido(email):
    return email and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

# =========================
# ENVIAR EMAIL
# =========================
def enviar_email(destinatario, nome, data, horario):
    try:
        msg = MIMEText(f"""
Olá {nome},

Sua aula foi agendada com sucesso!

📅 Data: {data}
⏰ Horário: {horario}

Até breve!
""")

        msg["Subject"] = "Aula Agendada"
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = destinatario

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        servidor.send_message(msg)
        servidor.quit()

    except Exception as e:
        print("Erro ao enviar email:", e)

# =========================
# DASHBOARD
# =========================
@app.route("/")
def dashboard():
    conn = conectar()

    alunos = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
    aulas = conn.execute("SELECT COUNT(*) FROM aulas").fetchone()[0]

    aulas_conteudo = [
        (row[0], row[1])
        for row in conn.execute("""
        SELECT conteudos.titulo, COUNT(*)
        FROM aulas
        JOIN conteudos ON aulas.conteudo_id = conteudos.id
        GROUP BY conteudos.titulo
        """).fetchall()
    ]

    conn.close()

    return render_template(
        "dashboard.html",
        alunos=alunos,
        aulas=aulas,
        aulas_conteudo=aulas_conteudo
    )

# =========================
# ALUNOS (GET + POST juntos)
# =========================
@app.route("/alunos", methods=["GET", "POST"])
def alunos():
    conn = conectar()

    if request.method == "POST":
        conn.execute(
            "INSERT INTO alunos (nome,email,telefone) VALUES (?,?,?)",
            (
                request.form["nome"],
                request.form["email"],
                request.form["telefone"]
            )
        )
        conn.commit()
        conn.close()
        return redirect("/alunos")

    lista = conn.execute("SELECT * FROM alunos").fetchall()
    conn.close()

    return render_template("alunos.html", alunos=lista)

# =========================
# EDITAR ALUNO
# =========================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = conectar()

    aluno = conn.execute(
        "SELECT * FROM alunos WHERE id=?", (id,)
    ).fetchone()

    if not aluno:
        conn.close()
        return "Aluno não encontrado", 404

    if request.method == "POST":
        conn.execute("""
        UPDATE alunos SET nome=?, email=?, telefone=? WHERE id=?
        """, (
            request.form["nome"],
            request.form["email"],
            request.form["telefone"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/alunos")

    conn.close()
    return render_template("editar.html", aluno=aluno)

# =========================
# EXCLUIR ALUNO
# =========================
@app.route("/excluir/<int:id>")
def excluir(id):
    conn = conectar()
    conn.execute("DELETE FROM alunos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/alunos")

# =========================
# AGENDA
# =========================
@app.route("/agenda")
def agenda():
    conn = conectar()

    alunos = conn.execute("SELECT id, nome FROM alunos").fetchall()
    conteudos = conn.execute("SELECT id, titulo FROM conteudos").fetchall()

    aulas = conn.execute("""
    SELECT aulas.id, alunos.nome, conteudos.titulo, aulas.data, aulas.horario
    FROM aulas
    JOIN alunos ON aulas.aluno_id = alunos.id
    JOIN conteudos ON aulas.conteudo_id = conteudos.id
    """).fetchall()

    conn.close()

    return render_template("agenda.html", alunos=alunos, conteudos=conteudos, aulas=aulas)

# =========================
# SALVAR AULA
# =========================
@app.route("/salvar_aula", methods=["POST"])
def salvar_aula():
    conn = conectar()

    conn.execute("""
    INSERT INTO aulas (aluno_id, conteudo_id, data, horario)
    VALUES (?, ?, ?, ?)
    """, (
        request.form["aluno_id"],
        request.form["conteudo_id"],
        request.form["data"],
        request.form["horario"]
    ))

    aluno = conn.execute(
        "SELECT nome, email FROM alunos WHERE id=?",
        (request.form["aluno_id"],)
    ).fetchone()

    conn.commit()
    conn.close()

    if aluno and email_valido(aluno["email"]):
        enviar_email(
            aluno["email"],
            aluno["nome"],
            request.form["data"],
            request.form["horario"]
        )

    return redirect("/agenda")

# =========================
# EDITAR AULA
# =========================
@app.route("/editar_aula/<int:id>", methods=["GET", "POST"])
def editar_aula(id):
    conn = conectar()

    if request.method == "POST":
        conn.execute("""
        UPDATE aulas
        SET aluno_id=?, conteudo_id=?, data=?, horario=?
        WHERE id=?
        """, (
            request.form["aluno_id"],
            request.form["conteudo_id"],
            request.form["data"],
            request.form["horario"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/agenda")

    aula = conn.execute("SELECT * FROM aulas WHERE id=?", (id,)).fetchone()
    alunos = conn.execute("SELECT id, nome FROM alunos").fetchall()
    conteudos = conn.execute("SELECT id, titulo FROM conteudos").fetchall()

    conn.close()

    return render_template("editar_aula.html", aula=aula, alunos=alunos, conteudos=conteudos)

# =========================
# EXCLUIR AULA
# =========================
@app.route("/excluir_aula/<int:id>")
def excluir_aula(id):
    conn = conectar()
    conn.execute("DELETE FROM aulas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/agenda")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)