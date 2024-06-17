import sqlite3

def main():


    id = 1

    with sqlite3.connect("./database.db") as con:
        cur = con.cursor()

        # Acessa a DB e pega id e senha de conta cujo email foi inserido pelo usuario
        try:
            
            #da adm
            cur.execute("UPDATE usuarios SET is_admin = 1 WHERE id = ?", (id,))
            #adiciona como vendedore
            cur.execute("INSERT INTO vendedores (usuario_id, verificado) VALUES (?,1)",(id,))
            con.commit()

        finally:
            cur.close


main()