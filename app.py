from ajudante import *
from cachelib.file import FileSystemCache
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import re
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__);
SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="/sessions"),
app.config.from_object(__name__)
Session(app)


@app.route("/registrar", methods=["GET","POST"])
def registrar():





    if (request.method == 'GET') :
        return render_template("registrar.html")

    else: # POST 
        # Checa se algum input foi deixado em branco
        if not all(request.form.values()):
            return render_template("registrar.html", infoFalta = True)
        
        checagem = {}
        checagem["emailInvalido"] = False
        checagem["senhasDiferente"] = False
        checagem["emailIndisponivel"] = False

        # Checa  se o email é valido
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not (re.fullmatch(regex, request.form.get("email"))):
            checagem["emailInvalido"] = True

        # Checa se senhas inseridas são iguais
        if (request.form.get("senha") != request.form.get("confirmSenha")):
            checagem["senhasDiferente"] = True

        if not checagem["emailInvalido"]:
            # Conecta na databse
            with sqlite3.connect("database/database.db") as con:
                cur = con.cursor()

                # TODO: mexer com a database
                try: 
                    # Checa se o email ja esta em uso
                    if cur.execute("SELECT 1 FROM usuarios WHERE email = ?", (request.form.get("email"),)).fetchone():
                        checagem["emailIndisponivel"] = True
                    
                    # TODO: Adicionar conta à DB 
                    if not any(checagem.values()): # Não executa se alguma checagem for verdade
                        pass
                finally:
                    cur.close()
        
        # Conta nao foi criada
        if any(checagem.values()):
                return render_template("registrar.html",
                                       senhasDiferente = checagem["senhasDiferente"], emailInvalido = checagem["emailInvalido"],
                                       emailIndisponivel = checagem["emailIndisponivel"])
        # Conta foi criada TODO:
        else:
            return "conta pode ser criada"
    
    