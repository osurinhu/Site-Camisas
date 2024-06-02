from flask import flash, render_template, redirect, session, url_for

def render_erro(mensagem="", codigo="400"):

    return render_template("error.html",mensagem=mensagem, codigo = codigo)

def login_necessario(func):
    def wrapper():
        if session.get("user_id"):
            return func()
        else:
            flash("É necessario entrar em uma conta","message")
            return redirect(url_for("autenticacao.entrar"))      
    return wrapper