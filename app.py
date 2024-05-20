from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cachelib.file import FileSystemCache
import sqlite3

app = Flask(__name__);
SESSION_TYPE = 'cachelib'
SESSION_SERIALIZATION_FORMAT = 'json'
SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="/sessions"),
app.config.from_object(__name__)
Session(app)


@app.route("/registrar", methods=["GET","POST"])
def register():


    if (request.method == 'GET') :
        return render_template("registrar.html");

    else:
        if request.form.get("name") == None or request.form.get("email") == None

        return
