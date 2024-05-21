from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cachelib.file import FileSystemCache
import sqlite3
from ajudante import *

app = Flask(__name__);
SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="/sessions"),
app.config.from_object(__name__)
Session(app)


@app.route("/registrar", methods=["GET","POST"])
def register():


    if (request.method == 'GET') :
        return render_template("registrar.html")

    else:

        # Checa se algum input foi deixado em branco
        if not all(request.form.values()):
            return render_erro("Dados em falta", "400")

        con = sqlite3.connect("database.db")


        return "teste"
