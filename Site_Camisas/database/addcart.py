import sqlite3

def main():


    id = 3

    with sqlite3.connect("./database.db") as con:
        cur = con.cursor()

        # Acessa a DB e pega id e senha de conta cujo email foi inserido pelo usuario
        try:
            
            for i in range(1,4):
                cur.execute("INSERT INTO cart (usuario_id, produto_id, qtd, data_adicao) VALUES (?,?,?,datetime('now'));", (id,i,i))



            con.commit()

        finally:
            cur.close


main()