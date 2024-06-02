from flask import Blueprint
from ..ajudantes.resources import login_necessario

admin_bp = Blueprint("admin", __name__, template_folder="templates" )

@admin_bp.route("/admin", methods=["GET", "POST"])
@login_necessario
def admin():



    return "tem vaga pra adm??"