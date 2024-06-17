from ..ajudantes.resources import login_necessario, login_necessario_fetch
from flask import Blueprint, redirect, request, render_template, session, jsonify
import sqlite3 
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR')


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

            carrinho = ()
            for item in itens:
                q_produto = cur.execute("SELECT produto_nome, produto_descricao, valor, desconto, vendedor_id FROM produtos WHERE id = ?", (item[0],)).fetchone()
                q_vendedor = cur.execute("SELECT nome FROM usuarios WHERE id = (SELECT usuario_id FROM vendedores WHERE id = ?);",(q_produto[4],)).fetchone()
                q_imagem = cur.execute("SELECT img_descricao, imagem FROM imagens_produtos WHERE produto_id = ?;",(item[0],)).fetchone()

                total = round(q_produto[2]*(1-(q_produto[3]/100))*item[1], 2)

                produto = {
                    "produto_id": item[0],
                    "qtd": item[1],
                    "produto_nome": q_produto[0],
                    "produto_descricao": q_produto[1],
                    "valor": locale.currency(q_produto[2], symbol=None),
                    "desconto": str(q_produto[3]).rstrip('0').rstrip('.').replace(".",","),
                    "atual": locale.currency((q_produto[2]*(1-(q_produto[3]/100))), symbol=None),
                    "total": locale.currency(total, symbol=None),
                    "vendedor": q_vendedor[0],
                    "descricao_img": q_imagem[0],
                    "imagem": q_imagem[1]
                }

                subtotal += total
                i+=1
                carrinho += (produto,)

        finally:
            cur.close()
    return render_template("cart.html",carrinho=carrinho, subtotal=subtotal, enumerate=enumerate)


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


@cartfav_bp.route("/favrm")
@login_necessario
def favrm():
    if not request.args.get("id"):
        return redirect("/favoritos")

    else:
        with sqlite3.connect("database/database.db") as con:
            try:
                cur = con.cursor()
                cur.execute("DELETE FROM favoritos WHERE produto_id = ? AND usuario_id = ?;",(request.args.get("id"),session["usuario_id"]))
                con.commit()

            finally:
                cur.close
        return redirect("favoritos")





@cartfav_bp.route("/cartqtd", methods=["GET"])
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

            

@cartfav_bp.route("/cartadd", methods=["POST"])
@login_necessario_fetch
def cartadd():
    inputs = {
        "act": request.form.get("act"),
        "produto_id": request.form.get("produto_id"),
        "qtd": request.form.get("qtd")
    }

    if not all(inputs.values()):
        return jsonify({"error": "falta info"}), 400
    
    if inputs["act"] == "insert":

        with sqlite3.connect("database/database.db") as con:
            try:
                cur = con.cursor()
                if cur.execute("SELECT 1 FROM cart WHERE produto_id = ? AND usuario_id = ?;",(inputs["produto_id"],session["usuario_id"])).fetchone():

                    # Atualizar db
                    cur.execute("UPDATE cart SET qtd = ? WHERE produto_id = ? AND usuario_id = ?",(request.form.get("qtd"),inputs["produto_id"],session["usuario_id"]))
                    return jsonify([{"message":"updatado"}])

                else:

                    cur.execute("INSERT INTO cart (usuario_id, produto_id, qtd, data_adicao) VALUES (?,?,?,datetime('now'));", (session["usuario_id"], inputs["produto_id"], inputs["qtd"]))
                    return jsonify([{"message":"adicionado"}])

                con.commit()

            finally:
                cur.close



@cartfav_bp.route("/favoritos")
@login_necessario
def favoritos():

    with sqlite3.connect("database/database.db") as con:
        try:
            cur = con.cursor()
            
            q_favs = cur.execute("SELECT id, produto_nome, valor, desconto FROM produtos WHERE id IN (SELECT produto_id FROM favoritos WHERE usuario_id = ?);",(session["usuario_id"],)).fetchall()

            favoritos = ()
            for produto in q_favs:

                q_imagem = cur.execute("SELECT img_descricao, imagem FROM imagens_produtos WHERE produto_id = ?;",(produto[0],)).fetchone()

                d_produto = {
                    "id": produto[0],
                    "produto_nome": produto[1],
                    "valor": locale.currency(produto[2], symbol=None),
                    "desconto": str(produto[3]).rstrip('0').rstrip('.').replace(".",","),
                    "atual": locale.currency((produto[2]*(1-(produto[3]/100))), symbol=None),
                    "descricao_img": q_imagem[0],
                    "imagem": q_imagem[1]
                }
                favoritos += (d_produto,)

        finally:
            cur.close()

    return render_template("fav.html", favoritos=favoritos)



@cartfav_bp.route("/favadd", methods=["POST"])
@login_necessario_fetch
def favadd():
    if not request.form.get("produto_id"):
        return jsonify([{"error":"informação em falta"}]), 400
    
    with sqlite3.connect("database/database.db") as con:
        try:
            cur = con.cursor()
            if cur.execute("SELECT 1 FROM favoritos WHERE produto_id = ? AND usuario_id = ?;",(request.form.get("produto_id"),session["usuario_id"])).fetchone():
                cur.execute("DELETE from favoritos WHERE produto_id = ? AND usuario_id = ?;",(request.form.get("produto_id"),session["usuario_id"]))
            else:
                cur.execute("INSERT INTO favoritos (usuario_id, produto_id, data_adicao) VALUES (?,?,datetime('now'));", (session["usuario_id"], request.form.get("produto_id")))

            con.commit()

        finally:
            cur.close()

    return jsonify([{"message":"favoritos atualizado"}]), 200