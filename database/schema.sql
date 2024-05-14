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

-- TODO: Preciso pensar mais
CREATE TABLE estampas (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    estampa_nome TEXT NOT NULL,
    estampa_descricao TEXT,
    price REAL NOT NULL,
    discount INTEGER,

	estampa_dono TEXT NOT NULL,
    add_date TEXT NOT NULL
)
	
CREATE TABLE tags (
    estampa_id INTEGER NOT NULL,
    tag TEXT NOT NULL,

    FOREIGN KEY(estampa_id) REFERENCES estampa_descricao(id)

)

CREATE TABLE favoritos (
    usuario_id INTEGER NOT NULL,
    estampa_id INTEGER NOT NULL,
    data_adicao TEXT NOT NULL,

    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(estampa_id) REFERENCES estampas(id)
)

CREATE TABLE cart (
    usuario_id INTEGER NOT NULL,
    estampa_id INTEGER NOT NULL,
    qtd INTEGER NOT NULL,
    data_adicao TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES usuarios(id),
    FOREIGN KEY(estampa_id) REFERENCES estampas(id)
);

