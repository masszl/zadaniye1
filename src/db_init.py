
import sqlite3
import os

def create_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect("db/shoe_store.sqlite")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS sizes (
        size_id INTEGER PRIMARY KEY AUTOINCREMENT,
        size_value REAL NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        login TEXT NOT NULL UNIQUE,
        role_id INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(role_id)
            ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT,
        manufacturer TEXT,
        price REAL NOT NULL CHECK(price > 0),
        image_path TEXT,
        composition TEXT,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS stock_items (
        stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        size_id INTEGER NOT NULL,
        quantity_available INTEGER NOT NULL DEFAULT 0
            CHECK(quantity_available >= 0),
        UNIQUE(product_id, size_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
            ON DELETE RESTRICT,
        FOREIGN KEY (size_id) REFERENCES sizes(size_id)
            ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Новый',
        FOREIGN KEY (user_id) REFERENCES users(user_id)
            ON DELETE RESTRICT
    );

    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        stock_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        price REAL NOT NULL CHECK(price > 0),
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
            ON DELETE CASCADE,
        FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id)
            ON DELETE RESTRICT
    );
    """)

    conn.commit()
    conn.close()
    print("База данных успешно создана")

if __name__ == "__main__":
    create_db()
