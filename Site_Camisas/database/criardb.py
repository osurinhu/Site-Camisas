import sqlite3

def main():

    with sqlite3.connect("./database.db") as con:
        cur = con.cursor()

        # Acessa a DB e pega id e senha de conta cujo email foi inserido pelo usuario
        try: 
                cur.execute("""CREATE TABLE  IF NOT EXISTS usuarios (
                    id INTEGER NOT NULL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    senha_hash TEXT NOT NULL,
                    telefone TEXT,
                    is_admin INTEGER, -- 1 = é adm, null/0 user comum

                    email_verificado INTEGER, -- 1 = verificado, null/0 não verificado
                    data_entrada TEXT NOT NULL,
                    senha_ultima_mudanca TEXT,
                    email_ultima_mudanca TEXT,
                    ultimo_login TEXT
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS endereco_usuario (
                    usuario_id INTEGER NOT NULL,
                    cep TEXT NOT NULL,
                    numero TEXT NOT NULL,

                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS favoritos (
                    usuario_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    data_adicao TEXT NOT NULL,

                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY(produto_id) REFERENCES produtos(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS cart (
                    usuario_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    qtd INTEGER NOT NULL,
                    data_adicao TEXT NOT NULL,

                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY(produto_id) REFERENCES produtos(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS compras (
                    usuario_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    qtd INTEGER NOT NULL,
                    forma_pagamento TEXT NOT NULL,
                    data_compra TEXT NOT NULL,


                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                );""")


                cur.execute("""CREATE TABLE  IF NOT EXISTS vendedores (
                    id INTEGER NOT NULL PRIMARY KEY,
                    usuario_id INTEGER NOT NULL,
                    verificado INTEGER,

                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS avaliacao_vendedor (
                    vendedor_id INTEGER NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    nota INTEGER NOT NULL, -- 1 a 5
                    comentario TEXT,

                    FOREIGN KEY(vendedor_id) REFERENCES vendedores(id),
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS produtos (
                    id INTEGER NOT NULL PRIMARY KEY,
                    produto_nome TEXT NOT NULL,
                    produto_descricao TEXT,
                    valor REAL NOT NULL,
                    desconto REAL,
                    data_adicao TEXT NOT NULL,
                    vendedor_id INTEGER NOT NULL,

                    FOREIGN KEY(vendedor_id) REFERENCES vendedores(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS tags (
                    produto_id INTEGER NOT NULL,
                    tag TEXT NOT NULL,

                    FOREIGN KEY(produto_id) REFERENCES produtos(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS views (
                    usuario_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    qtd_views INTEGER NOT NULL,
                    data_view TEXT NOT NULL,

                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY(tag_id) REFERENCES tags(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS imagens_produtos(
                    id INTEGER NOT NULL PRIMARY KEY,
                    produto_id INTEGER NOT NULL,
                    img_descricao TEXT,
                    imagem BLOB NOT NULL,

                    FOREIGN KEY(produto_id) REFERENCES produtos(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS avaliacoes_produtos (
                    id INTEGER NOT NULL PRIMARY KEY,
                    produto_id INTEGER NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    nota INTEGER NOT NULL, -- 1 a 5
                    comentario TEXT,

                    FOREIGN KEY(produto_id) REFERENCES produtos(id),
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                );""")

                cur.execute("""CREATE TABLE  IF NOT EXISTS imagens_avaliacoes(
                    id INTEGER NOT NULL PRIMARY KEY,
                    avaliacao_id INTEGER NOT NULL,
                    img_descricao TEXT,
                    imagem BLOB NOT NULL,

                    FOREIGN KEY(avaliacao_id) REFERENCES avaliacoes_produto(id)
                );""")

                con.commit()
            
        finally:
            cur.close()

main()