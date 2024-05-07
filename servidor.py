from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__);

@app.route("/login", methods=["GET","POST"])
def index():
    return render_template("login.html");