from ajudante import *
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import os
import re
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'database/'
app.config['SESSION_FILE_THRESHOLD'] = 500


@app.route("/registrar", methods=["GET","POST"])
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
            flash("Informações em falta")
            return redirect("/registrar")
        
        # Define variavies para checagem da validez dos inputs
        checagem = {
            "emailInvalido": False,
            "senhasDiferente": False,
            "emailIndisponivel": False
        }

        # Checa se o email é valido
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not (re.fullmatch(regex, request.form.get("email"))):
            checagem["emailInvalido"] = True
            flash("Email invalido")

        # Checa se senhas inseridas são iguais
        if (user_input["senha"] != user_input["confirmSenha"]):
            checagem["senhasDiferente"] = True
            flash("Senhas não correspondem")

        if not checagem["emailInvalido"]: # Não conecta na DB caso email seja invalido
            # Conecta na databse
            with sqlite3.connect("database/database.db") as con:
                cur = con.cursor()

                # TODO: mexer com a database
                try: 
                    # Checa se o email ja esta em uso
                    if cur.execute("SELECT 1 FROM usuarios WHERE email = ?", (user_input["email"],)).fetchone():
                        checagem["emailIndisponivel"] = True
                        flash("Email já é utilizado por uma conta")
                    
                    # Adicionar conta à DB 
                    if not any(checagem.values()): # Não executa se alguma checagem for verdade
                        cur.execute("INSERT INTO usuarios (nome, email, senha_hash, data_entrada) VALUES (?, ?, ?, datetime('now', 'localtime'));",
                                    (user_input["nome"], user_input["email"], generate_password_hash(user_input["senha"])))
                        con.commit()

                        

            
                finally:
                    cur.close()
        
        # Conta nao foi criada
        if any(checagem.values()):
                return render_template("registrar.html")
        
        
        # Conta foi criada TODO:
        return "conta pode ser criada"
    
    

if __name__ == '__main__':
    app.run(debug=True)