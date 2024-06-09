from ..ajudantes.resources import apenas_admin, render_erro
import base64
from flask import Blueprint, render_template, redirect, request, session
import sqlite3

admin_bp = Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")

@admin_bp.route("/", methods=["GET"])
@apenas_admin
def admin():

    with sqlite3.connect("database/database.db") as con:
        cur = con.cursor()
        try:
            query = cur.execute("SELECT * FROM produtos WHERE vendedor_id = ?;",(session["usuario_id"],)).fetchall()

            i = 0
            for produto in query:

                imagem = cur.execute("SELECT id, img_descricao, imagem FROM imagens_produtos WHERE produto_id = ?;",(produto[0],)).fetchall()
                
                
                query[i] += (imagem,)
                i += 1
                

        finally:
            cur.close()


    return render_template("admin.html",query=query)
















@admin_bp.route("/adicionar_produto", methods=["GET", "POST"])
@apenas_admin
def adicionar_produto():
        
    if request.method == "GET":
        return render_template("adicionar_produto.html")
    
    else:

        user_inputs = {
            "produto_nome": request.form.get("produto_nome"),
            "produto_descricao": request.form.get("produto_descricao"),
            "valor": request.form.get("valor"),
            "desconto": request.form.get("desconto"),
            "img_descricao": request.form.get("img_descricao"),
            "img": []
        }

        files = request.files.getlist('imagem')
        for imagem in files:
            user_inputs["img"].append(base64.b64encode(imagem.read()).decode('utf-8'))


        
        if not all(user_inputs.values()):
            return render_erro("informação em falta")
        
        # Converte inputs em float
        user_inputs["valor"] = float(user_inputs["valor"])
        user_inputs["desconto"] = float(user_inputs["desconto"])


        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()

            # Acessa a DB e adiciona produto
            try: 
                cur.execute("INSERT INTO produtos (produto_nome, produto_descricao, valor, desconto, data_adicao, vendedor_id) VALUES (?,?,?,?,datetime('now', 'localtime'),?);",(user_inputs["produto_nome"],user_inputs["produto_descricao"],user_inputs["valor"],user_inputs["desconto"],session["usuario_id"]))
                produto_id = cur.lastrowid

                for imagem in user_inputs["img"]:
                    cur.execute("INSERT INTO imagens_produtos (produto_id, img_descricao, imagem) VALUES (?,?,?);",(produto_id, user_inputs["img_descricao"],imagem))
                con.commit()

            finally:
                cur.close()


        return redirect("/admin")