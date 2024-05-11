-- TODO: Preciso pensar mais
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    phone_number TEXT,
    email TEXT NOT NULL,
    pw_hash TEXT NOT NULL,

    join_date TEXT NOT NULL,
    last_pw_change TEXT,
    last_email_change TEXT,
    last_login TEXT
)
-- TODO: Preciso pensar mais TODO: vendedor
CREATE TABLE products (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_description TEXT,
    price REAL NOT NULL,
    discount INTEGER,

    add_date TEXT NOT NULL
)

CREATE TABLE tags (

    product_id INTEGER NOT NULL,
    tag TEXT NOT NULL,

    FOREIGN KEY(product_id_id) REFERENCES products(id)

)

CREATE TABLE favorites (
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    add_date TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id_id) REFERENCES products(id)
)

CREATE TABLE cart (
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qtd INTEGER NOT NULL,
    add_date TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id_id) REFERENCES products(id)
)

