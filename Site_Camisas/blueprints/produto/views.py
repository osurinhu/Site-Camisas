from flask import Blueprint, render_template, request
import sqlite3

produto_bp =  Blueprint("produto_bp", __name__, template_folder="templates", url_prefix="/produto")



@produto_bp.route("/")
def asd():
    return render_template("produto.html")



@produto_bp.route("/<produto_id>", methods=["GET", "POST"])
def produto(produto_id):
    if request.method == "GET":

        # Conecta na databse
        with sqlite3.connect("database/database.db") as con:
            cur = con.cursor()

            # Acessa a DB e pega id e senha de conta cujo email foi inserido pelo usuario
            try: 
                q_produto = cur.execute("SELECT produto_nome, produto_descricao, valor, desconto, vendedor_id FROM produtos WHERE id = ?;", (produto_id,)).fetchone()

                q_vendedor = cur.execute("SELECT nome FROM usuarios WHERE id = (SELECT usuario_id FROM vendedores WHERE id =?);",(q_produto[4],)).fetchone()

                q_imagens = cur.execute("SELECT img_descricao, imagem FROM imagens_produtos WHERE produto_id = ?;",(produto_id,)).fetchall()

                query = q_produto + ((q_produto[2]*(1-(q_produto[3]/100))),) + q_vendedor + (q_imagens,)

                
            finally:
                cur.close()
                
        return str(query)


        return render_template("produto.html")
