from flask import Blueprint, render_template
import sqlite3

produto_bp =  Blueprint("produto_bp", __name__, template_folder="templates", url_prefix="/produto")


@produto_bp.route("/")
def produto():
    return render_template("produto.html")
