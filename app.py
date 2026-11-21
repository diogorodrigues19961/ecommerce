
import sqlite3
from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "mens_store_chave_secreta_2026"


# CRIAR BANCO DE DADOS
def criar_banco():

    conexao = sqlite3.connect("banco.db")

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()


criar_banco()


# PÁGINA INICIAL
@app.route("/")
def inicio():

    return render_template("index.html")


# CADASTRO DE CLIENTES
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"].strip()
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        # VALIDAR SENHA
        if (
            len(senha) < 12
            or not any(letra.isupper() for letra in senha)
            or not any(letra.islower() for letra in senha)
            or not any(letra.isdigit() for letra in senha)
        ):

            return render_template(
                "cadastro.html",
                mensagem="A senha precisa ter 12 caracteres, uma letra maiúscula, uma minúscula e um número."
            )

        # PROTEGER SENHA
        senha_protegida = generate_password_hash(senha)

        conexao = sqlite3.connect("banco.db")

        try:

            conexao.execute(
                "INSERT INTO clientes (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_protegida)
            )

            conexao.commit()

            mensagem = "Cadastro realizado com sucesso!"

        except sqlite3.IntegrityError:

            mensagem = "Este e-mail já está cadastrado."

        finally:

            conexao.close()

        return render_template(
            "cadastro.html",
            mensagem=mensagem
        )

    return render_template("cadastro.html")


# LOGIN DE CLIENTES
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id, nome, senha FROM clientes WHERE email = ?",
            (email,)
        )

        cliente = cursor.fetchone()

        conexao.close()

        if cliente and check_password_hash(cliente[2], senha):

            session["cliente_id"] = cliente[0]
            session["cliente_nome"] = cliente[1]

            return redirect("/minha-conta")

        else:

            mensagem = "E-mail ou senha incorretos."

            return render_template(
                "login.html",
                mensagem=mensagem
            )

    return render_template("login.html")


# MINHA CONTA
@app.route("/minha-conta")
def minha_conta():

    if "cliente_id" not in session:

        return redirect("/login")

    nome = session["cliente_nome"]

    return render_template(
        "minha_conta.html",
        nome=nome
    )


# SAIR DA CONTA
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# EDITAR DADOS DA CONTA
@app.route("/editar-conta", methods=["GET", "POST"])
def editar_conta():

    if "cliente_id" not in session:

        return redirect("/login")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    mensagem = ""

    if request.method == "POST":

        nome = request.form["nome"].strip()
        email = request.form["email"].strip().lower()

        try:

            cursor.execute(
                "UPDATE clientes SET nome = ?, email = ? WHERE id = ?",
                (nome, email, session["cliente_id"])
            )

            conexao.commit()

            session["cliente_nome"] = nome

            mensagem = "Dados atualizados com sucesso!"

        except sqlite3.IntegrityError:

            mensagem = "Este e-mail já está cadastrado."

    cursor.execute(
        "SELECT nome, email FROM clientes WHERE id = ?",
        (session["cliente_id"],)
    )

    cliente = cursor.fetchone()

    conexao.close()

    return render_template(
        "editar_conta.html",
        nome=cliente[0],
        email=cliente[1],
        mensagem=mensagem
    )


# ALTERAR SENHA
@app.route("/alterar-senha", methods=["GET", "POST"])
def alterar_senha():

    if "cliente_id" not in session:

        return redirect("/login")

    mensagem = ""

    if request.method == "POST":

        senha_atual = request.form["senha_atual"]
        nova_senha = request.form["nova_senha"]
        confirmar_senha = request.form["confirmar_senha"]

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT senha FROM clientes WHERE id = ?",
            (session["cliente_id"],)
        )

        cliente = cursor.fetchone()

        if not cliente:

            conexao.close()
            session.clear()

            return redirect("/login")

        if not check_password_hash(cliente[0], senha_atual):

            mensagem = "A senha atual está incorreta."

        elif nova_senha != confirmar_senha:

            mensagem = "As novas senhas não coincidem."

        elif (
            len(nova_senha) < 12
            or not any(letra.isupper() for letra in nova_senha)
            or not any(letra.islower() for letra in nova_senha)
            or not any(letra.isdigit() for letra in nova_senha)
        ):

            mensagem = "A nova senha precisa ter 12 caracteres, uma letra maiúscula, uma minúscula e um número."

        else:

            senha_protegida = generate_password_hash(nova_senha)

            cursor.execute(
                "UPDATE clientes SET senha = ? WHERE id = ?",
                (senha_protegida, session["cliente_id"])
            )

            conexao.commit()

            mensagem = "Senha alterada com sucesso!"

        conexao.close()

    return render_template(
        "alterar_senha.html",
        mensagem=mensagem
    )

# RECUPERAR SENHA
@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():

    mensagem = ""

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id FROM clientes WHERE email = ?",
            (email,)
        )

        cliente = cursor.fetchone()

        conexao.close()

        if cliente:
            mensagem = "Se o e-mail estiver cadastrado, você receberá as instruções de recuperação."
        else:
            mensagem = "Se o e-mail estiver cadastrado, você receberá as instruções de recuperação."

    return render_template(
        "recuperar_senha.html",
        mensagem=mensagem
    )


# INICIAR A APLICAÇÃO
if __name__ == "__main__":

    app.run(debug=True)
