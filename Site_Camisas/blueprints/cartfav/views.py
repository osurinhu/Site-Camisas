from ..ajudantes.resources import login_necessario
from flask import Blueprint, redirect, request, render_template, session
import sqlite3



cartfav_bp = Blueprint("cartfav", __name__, template_folder="templates")

@cartfav_bp.route("/carrinho")
@login_necessario
def carrinho():

    with sqlite3.connect("database/database.db") as con:
        try:
            cur = con.cursor()
            itens = cur.execute("SELECT produto_id, qtd FROM cart WHERE usuario_id = ?;",(session["usuario_id"],)).fetchall()

            i = 0
            subtotal = 0

            for item in itens:
                q_produto = cur.execute("SELECT produto_nome, produto_descricao, valor, desconto, vendedor_id FROM produtos WHERE id = ?", (item[0],)).fetchone()
                q_vendedor = cur.execute("SELECT nome FROM usuarios WHERE id = (SELECT usuario_id FROM vendedores WHERE id = ?);",(q_produto[4],)).fetchone()
                q_imagem = cur.execute("SELECT img_descricao, imagem FROM imagens_produtos WHERE produto_id = ?;",(item[0],)).fetchone()
                total = round(q_produto[2]*(1+(q_produto[3]/100))*item[1], 2)
                subtotal += total
                itens[i] = itens[i] + q_produto + (total,) + q_vendedor + q_imagem
                i+=1
        finally:
            cur.close()
    return render_template("cart.html",itens=itens, subtotal=subtotal)


@cartfav_bp.route("/cartrm")
@login_necessario
def cartrm():
    if not request.args.get("id"):
        return redirect("/carrinho")

    else:
        with sqlite3.connect("database/database.db") as con:
            try:
                cur = con.cursor()
                cur.execute("DELETE FROM cart WHERE produto_id = ? AND usuario_id = ?;",(request.args.get("id"),session["usuario_id"]))
                con.commit()

            finally:
                cur.close
        return redirect("carrinho")
    
@cartfav_bp.route("/cartqtd")
@login_necessario
def cartqtd():
    if not (request.args.get("id") and isinstance(int(request.args.get("qtd")),int) and (request.args.get("act") == "add" or request.args.get("act") == "sub")):
        return redirect("/carrinho")
    
    else:
        if request.args.get("act") == "add":
            n_qtd = int(request.args.get("qtd")) + 1
        else:
            n_qtd = int(request.args.get("qtd")) - 1
            if n_qtd < 0:
                n_qtd = 0

        with sqlite3.connect("database/database.db") as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE cart SET qtd = ? WHERE produto_id = ? AND usuario_id = ?;",(n_qtd, request.args.get("id"), session["usuario_id"]))
                con.commit()

            finally:
                cur.close
            return redirect("/carrinho")
    
