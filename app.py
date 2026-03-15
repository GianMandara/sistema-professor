from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def dashboard():

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM alunos")
    total_alunos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM aulas")
    total_aulas = cursor.fetchone()[0]

    conn.close()

    return render_template("dashboard.html", alunos=total_alunos, aulas=total_aulas)


@app.route("/alunos")
def alunos():

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")
    lista = cursor.fetchall()

    conn.close()

    return render_template("alunos.html", alunos=lista)


@app.route("/salvar_aluno", methods=["POST"])
def salvar_aluno():

    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO alunos (nome,email,telefone) VALUES (?,?,?)",
        (nome, email, telefone)
    )

    conn.commit()
    conn.close()

    return redirect("/alunos")

@app.route("/agenda")
def agenda():

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    # buscar alunos
    cursor.execute("SELECT id, nome FROM alunos")
    alunos = cursor.fetchall()

    # buscar conteúdos
    cursor.execute("SELECT id, titulo FROM conteudos")
    conteudos = cursor.fetchall()

    # buscar aulas
    cursor.execute("""
    SELECT aulas.id, alunos.nome, conteudos.titulo, aulas.data, aulas.horario
    FROM aulas
    JOIN alunos ON aulas.aluno_id = alunos.id
    JOIN conteudos ON aulas.conteudo_id = conteudos.id
    """)

    aulas = cursor.fetchall()

    conn.close()

    return render_template(
        "agenda.html",
        alunos=alunos,
        conteudos=conteudos,
        aulas=aulas
    )

@app.route("/salvar_aula", methods=["POST"])
def salvar_aula():

    aluno_id = request.form["aluno_id"]
    conteudo_id = request.form["conteudo_id"]
    data = request.form["data"]
    horario = request.form["horario"]

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO aulas (aluno_id, conteudo_id, data, horario)
    VALUES (?, ?, ?, ?)
    """, (aluno_id, conteudo_id, data, horario))

    conn.commit()
    conn.close()

    return redirect("/agenda")

@app.route("/excluir_aula/<int:id>")
def excluir_aula(id):

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM aulas WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/agenda")

@app.route("/editar_aula/<int:id>")
def editar_aula(id):

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, aluno_id, conteudo_id, data, horario
    FROM aulas
    WHERE id=?
    """,(id,))

    aula = cursor.fetchone()

    cursor.execute("SELECT id, nome FROM alunos")
    alunos = cursor.fetchall()

    cursor.execute("SELECT id, titulo FROM conteudos")
    conteudos = cursor.fetchall()

    conn.close()

    return render_template(
        "editar_aula.html",
        aula=aula,
        alunos=alunos,
        conteudos=conteudos
    )

@app.route("/atualizar_aula", methods=["POST"])
def atualizar_aula():

    id = request.form["id"]
    aluno_id = request.form["aluno_id"]
    conteudo_id = request.form["conteudo_id"]
    data = request.form["data"]
    horario = request.form["horario"]

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE aulas
    SET aluno_id=?, conteudo_id=?, data=?, horario=?
    WHERE id=?
    """,(aluno_id,conteudo_id,data,horario,id))

    conn.commit()
    conn.close()

    return redirect("/agenda")

@app.route("/excluir_aluno/<int:id>")
def excluir_aluno(id):

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alunos WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/alunos")

@app.route("/editar_aluno/<int:id>")
def editar_aluno(id):

    conn = sqlite3.connect("database/escola.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos WHERE id = ?", (id,))
    aluno = cursor.fetchone()

    conn.close()

    return render_template("editar_aluno.html", aluno=aluno)

if __name__ == "__main__":
    app.run(debug=True)