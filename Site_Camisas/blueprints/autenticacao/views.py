from flask import Blueprint, flash, redirect, render_template, request, session
import re
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

autenticacao_bp = Blueprint("autenticacao", __name__, template_folder="templates")

@autenticacao_bp.route("/registrar", methods=["GET","POST"])
def registrar():
    if (request.method == 'GET') :
        return render_template("registrar.html")

    else: # POST 
        
        # Filtra inputs
        user_input = {
            "nome": request.form.get("nome"),
            "email": request.form.get("email"),
            "senha": request.form.get("senha"),
            "confirmSenha": request.form.get("confirmSenha")
        }

        # Checa se algum input foi deixado em branco
        if not all(user_input.values()):
            flash("Informações em falta","info")
            return redirect("/registrar")
        
        # Checa se o email é valido
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not (re.fullmatch(regex, request.form.get("email"))):
            flash("Email fora do padrão","info")
        

        infoValidas = True

        # Checa se senhas inseridas são iguais
        if (user_input["senha"] != user_input["confirmSenha"]):
            infoValidas = False
            flash("Senhas não correspondem","info")

        # Conecta na databse
        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()

            # TODO: mexer com a database
            try: 
                # Checa se o email ja esta em uso
                if cur.execute("SELECT 1 FROM usuarios WHERE email = ?", (user_input["email"],)).fetchone():
                    infoValidas = False
                    flash("Email já é utilizado por uma conta","info")
                
                if not infoValidas: # Caso conta NÃO possa ser criada
                    return redirect("/registrar")
                
                else:# Caso conta POSSA ser criada
                    # Adicionar conta à DB
                    cur.execute("INSERT INTO usuarios (nome, email, senha_hash, data_entrada) VALUES (?, ?, ?, datetime('now', 'localtime'));",
                                (user_input["nome"], user_input["email"], generate_password_hash(user_input["senha"])))
                    con.commit()

                    # Conta foi criada, redirecionar ao login
                    flash("Conta Criada","message")
                    return redirect("/entrar")

            finally:
                cur.close()
        
    
@autenticacao_bp.route("/entrar", methods=["GET","POST"])
def entrar():
    if request.method == "GET":
        return render_template("login.html")
    
    else:   

        # Filtra inputs do usuario    
        user_input = {
            "email": request.form.get("email"),
            "senha": request.form.get("senha")
        }

        # Checa se todos inputs foram preenchidos
        if not all(user_input.values()):
            flash("Informações em falta","info")
            return redirect("/entrar")
        
        # Conecta na databse
        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()

            # Acessa a DB e pega id e senha de conta cujo email foi inserido pelo usuario
            try: 
                query = cur.execute("SELECT id, senha_hash FROM usuarios WHERE email = ?", (user_input["email"],)).fetchall()
                
            finally:
                cur.close()
        
        # Checa se há correspondencia de email na DB
        if len(query) != 1:
            flash("Email e/ou senha incorretos","info")
            return redirect("/entrar")

        # Checa se a senha inserida pelo usuario corresponde com a da DB
        if not check_password_hash(query[0][1], user_input["senha"]):
            flash("Email e/ou senha incorretos","info")
            return redirect("/entrar")
        

        else:

            # TODO: depois de logar
            session["usuario_id"] = query[0][0]
            return "logado"

