-- IMPORTANTE https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm


-- TODO: Preciso pensar mais
CREATE TABLE usuarios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    numero_telefone TEXT,
    email TEXT NOT NULL,
    senha_hash TEXT NOT NULL,

    data_entrada TEXT NOT NULL,
    senha_ultima_mudanca TEXT,
    email_ultima_mudanca TEXT,
    ultimo_login TEXT
)

CREATE TABLE endereco_user (
    cep TEXT NOT NULL,
    numero TEXT NOT NULL,    
)

-- TODO: Preciso pensar mais
CREATE TABLE produtos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    produto_nome TEXT NOT NULL,
    produto_descricao TEXT,
    valor REAL NOT NULL,
    desconto REAL,
    data_adicao TEXT NOT NULL,
    nota INTEGER NOT NULL
)
	
CREATE TABLE tags (
    produto_id INTEGER NOT NULL,
    tag TEXT NOT NULL,

    FOREIGN KEY(produto_id) REFERENCES produto_descricao(id)
)

CREATE TABLE imagens(

    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    img_descricao TEXT,

    imagem BLOB NOT NULL
)

CREATE TABLE favoritos (
    usuario_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    data_adicao TEXT NOT NULL,

    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
)

CREATE TABLE cart (
    usuario_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    qtd INTEGER NOT NULL,
    data_adicao TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES usuarios(id),
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
);

CREATE TABLE views (
    user_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    qtd_views INTEGER NOT NULL,

    FOREIGN KEY(user_id) REFERENCES usuarios(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
)

CREATE TABLE compras (
    user_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    qtd INTEGER NOT NULL,
    forma_pagamento TEXT NOT NULL,
    data_compra TEXT NOT NULL,


    FOREIGN KEY(user_id) REFERENCES usuarios(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
)