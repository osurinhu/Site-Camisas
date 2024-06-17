from flask import Blueprint, request, render_template
import sqlite3
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR')

pesquisa_bp = Blueprint("pesquisa", __name__, template_folder="templates")


@pesquisa_bp.route("/pesquisa")
def pesquisa():
        
    with sqlite3.connect("database/database.db") as con:
        try:
            cur = con.cursor()
            

            q_pesquisa = cur.execute("""SELECT 
    produtos.id, 
    produtos.produto_nome, 
    produtos.valor, 
    produtos.desconto 
FROM 
    produtos
WHERE 
    produtos.id IN (
        SELECT produto_id 
        FROM tags 
        WHERE tag LIKE '%' || ? || '%'
    )
    OR produtos.id IN (
        SELECT id 
        FROM produtos 
        WHERE produto_nome LIKE '%' || ? || '%'
    )
    OR produtos.id IN (
        SELECT id 
        FROM produtos 
        WHERE produto_descricao LIKE '%' || ? || '%'
    )
    OR produtos.id IN (
        SELECT produtos.id
        FROM produtos
        JOIN vendedores ON produtos.vendedor_id = vendedores.id
        JOIN usuarios ON vendedores.usuario_id = usuarios.id
        WHERE usuarios.nome LIKE '%' || ? || '%'
    );
""",(request.args.get("q"),request.args.get("q"),request.args.get("q"),request.args.get("q"))).fetchall()

            pesquisa = ()
            for produto in q_pesquisa:

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
                pesquisa += (d_produto,)

        finally:
            cur.close()

    return render_template("pesquisa.html", pesquisa=pesquisa, resultados=len(pesquisa))

