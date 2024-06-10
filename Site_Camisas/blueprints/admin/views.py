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
                tags = cur.execute("SELECT tag FROM tags WHERE produto_id = ?;",(produto[0],)).fetchall()
                query[i] += (tags,imagem)
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
        # Filtra inputs
        user_inputs = {
            "produto_nome": request.form.get("produto_nome"),
            "produto_descricao": request.form.get("produto_descricao"),
            "valor": request.form.get("valor"),
            "desconto": request.form.get("desconto"),
            "img_descricao": request.form.get("img_descricao"),
            "tags": request.form.get("tags"),
            "img": []
        }

        # Transforma imagens (se tiver)em base64
        files = request.files.getlist('imagem')
        for imagem in files:
            user_inputs["img"].append(base64.b64encode(imagem.read()).decode('utf-8'))


        # Checa se todos os campos foram preenchidos
        if not all(user_inputs.values()):
            return render_erro("informação em falta")
        
        # Converte inputs em float
        user_inputs["valor"] = float(user_inputs["valor"])
        user_inputs["desconto"] = float(user_inputs["desconto"])

        # Transforma string de tags em lista
        user_inputs["tags"] = user_inputs["tags"].split(",")


        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()

            # Acessa a DB e adiciona produto
            try: 
                # Adiciona produto
                cur.execute("INSERT INTO produtos (produto_nome, produto_descricao, valor, desconto, data_adicao, vendedor_id) VALUES (?,?,?,?,datetime('now', 'localtime'),?);",(user_inputs["produto_nome"],user_inputs["produto_descricao"],user_inputs["valor"],user_inputs["desconto"],session["usuario_id"]))
                
                # Pega id do produto adicionado
                produto_id = cur.lastrowid

                # Adiciona imagens
                for imagem in user_inputs["img"]:
                    cur.execute("INSERT INTO imagens_produtos (produto_id, img_descricao, imagem) VALUES (?,?,?);",(produto_id, user_inputs["img_descricao"],imagem))
                
                # Adiciona tags
                for tag in user_inputs["tags"]:
                    if tag:
                        cur.execute("INSERT INTO tags (produto_id, tag) VALUES (?,?)",(produto_id,tag))
                con.commit()

            finally:
                cur.close()

        return redirect("/admin")
    

@admin_bp.route("/remover_produto", methods = ["GET"])
@apenas_admin
def remover_produto():

    if int(request.args.get("r",False)):
    
        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()
        try:
            if cur.execute("SELECT 1 FROM produtos WHERE id = ? AND vendedor_id = ?;",(request.args.get("r"), session["usuario_id"])).fetchone():
                cur.execute("DELETE FROM produtos WHERE id = ?;",(request.args.get("r"),))
                cur.execute("DELETE FROM tags WHERE produto_id = ?;",(request.args.get("r"),))
                cur.execute("DELETE FROM imagens_produtos WHERE produto_id = ?;",(request.args.get("r"),))
                con.commit()
            else:
               return render_erro("Id do produto não corresponde a um produto deste usuario", "403")
        finally:
            cur.close()

        return redirect("/admin/remover_produto")

    else:
        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()
        try:

            query = cur.execute("SELECT id, produto_nome, produto_descricao FROM produtos WHERE vendedor_id = ?;",(session["usuario_id"],)).fetchall()

        finally:
            cur.close()

        return render_template("remover_produto.html", query = query)