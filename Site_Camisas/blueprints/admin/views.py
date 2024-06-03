from ..ajudantes.resources import apenas_admin, login_necessario, render_erro
from flask import Blueprint, render_template, request, session
import sqlite3

admin_bp = Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")
@admin_bp.route("/", methods=["GET"])
@apenas_admin
def admin():
    return render_template("base_admin.html")


@admin_bp.route("/adicionar_produto", methods=["GET", "POST"])
@apenas_admin
def adicionar_produto():
        
    if request.method == "GET":
        return render_template("adicionar_produto.html")
    
    else:






        return "bulhufas"
