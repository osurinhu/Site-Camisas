from flask import flash, render_template, redirect, session, url_for
import sqlite3

def render_erro(mensagem="", codigo="400"):

    return render_template("error.html",mensagem=mensagem, codigo = codigo), codigo

def login_necessario(funcao):
    def wrapper():
        if not session.get("user_id"):
            return redirect(url_for("autenticacao.entrar"))

        # Conecta na DB 
        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()
        # Acessa DB
        try: 
            # Checa se conta existe com id da sessão
            if cur.execute("SELECT 1 FROM usuarios WHERE id = ?", (session.get("user_id"),)).fetchone():
                return funcao()
            else:
                return redirect(url_for("autenticacao.entrar"))
        # Fecha DB
        finally:
            cur.close()

    return wrapper



def apenas_admin(funcao):
    @login_necessario
    def wrapper():
            # Conecta na DB 
        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()
        # Acessa DB
        try: 
            is_admin = cur.execute("SELECT is_admin FROM usuarios WHERE id = ?", (session["user_id"],)).fetchall()
        # Fecha DB
        finally:
            cur.close()

        # Checa se o usuario é adm
        if not is_admin[0][0]:
            return render_erro("Acesso negado","403")
        else:
            return funcao()
    return wrapper