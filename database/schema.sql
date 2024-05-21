-- IMPORTANTE https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

-- ************ USUARIOs *******************

CREATE TABLE usuarios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    usuario TEXT NOT NULL,
    email TEXT NOT NULL,
    senha_hash TEXT NOT NULL,

    data_entrada TEXT NOT NULL,
    senha_ultima_mudanca TEXT,
    email_ultima_mudanca TEXT,
    ultimo_login TEXT
);

CREATE TABLE endereco_usuario (
    usuario_id INTEGER NOT NULL,
    cep TEXT NOT NULL,
    numero TEXT NOT NULL,

    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE favoritos (
    usuario_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    data_adicao TEXT NOT NULL,

    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
);

CREATE TABLE cart (
    usuario_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    qtd INTEGER NOT NULL,
    data_adicao TEXT NOT NULL,

    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
);

CREATE TABLE compras (
    usuario_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    qtd INTEGER NOT NULL,
    forma_pagamento TEXT NOT NULL,
    data_compra TEXT NOT NULL,


    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);


CREATE TABLE vendedores (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    verificado INTEGER,

    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE avaliacao_vendedor (
    vendedor_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    nota INTEGER NOT NULL, -- 1 a 5
    comentario TEXT,

    FOREIGN KEY(vendedor_id) REFERENCES vendedores(id),
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

-- ************** PRODUTOS ****************

CREATE TABLE produtos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    produto_nome TEXT NOT NULL,
    produto_descricao TEXT,
    valor REAL NOT NULL,
    desconto REAL,
    data_adicao TEXT NOT NULL,
    vendedor_id INTEGER NOT NULL,

    FOREIGN KEY(vendedor_id) REFERENCES vendedores(id)
);

CREATE TABLE tags (
    produto_id INTEGER NOT NULL,
    tag TEXT NOT NULL,

    FOREIGN KEY(produto_id) REFERENCES produtos(id)
);

CREATE TABLE views (
    usuario_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    qtd_views INTEGER NOT NULL,
    data_view TEXT NOT NULL,

    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);

CREATE TABLE imagens_produtos(

    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    img_descricao TEXT,
    imagem BLOB NOT NULL,

    FOREIGN KEY(produto_id) REFERENCES produtos(id)
);

CREATE TABLE avaliacoes_produtos (
    id INTEGER NOT NULL AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    nota INTEGER NOT NULL, -- 1 a 5
    comentario TEXT,

    FOREIGN KEY(produto_id) REFERENCES produtos(id),
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE imagens_avaliacoes(

    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    avaliacao_id INTEGER NOT NULL,
    img_descricao TEXT,
    imagem BLOB NOT NULL,

    FOREIGN KEY(avaliacao_id) REFERENCES avaliacoes_produto(id)
);