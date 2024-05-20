from flask import render_template, redirect

def render_erro(mensagem="", codigo="400"):

    return render_template("error.html")