from flask import Blueprint, render_template
import sqlite3
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR')

index_bp = Blueprint("index", __name__, template_folder="templates")

@index_bp.route("/")
def index():

    with sqlite3.connect("database/database.db") as con:
        try:
            cur = con.cursor()
            
            q_custom = cur.execute("SELECT id, produto_nome, valor, desconto FROM produtos WHERE id IN (SELECT produto_id FROM tags WHERE tag LIKE '%custom%')").fetchall()

            custom = ()
            for produto in q_custom:

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
                custom += (d_produto,)


            q_lotuz = cur.execute("SELECT id, produto_nome, valor, desconto FROM produtos WHERE produto_nome LIKE '%' || 'LOTUZ' || '%'").fetchall()

            lotuz = ()
            for produto in q_lotuz:

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
                lotuz += (d_produto,)



        finally:
            cur.close()

    return render_template("index.html",custom=custom, lotuz=lotuz ,len=len, enumerate=enumerate, round=round)