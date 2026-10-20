import sqlite3

conn = sqlite3.connect("db/shoe_store.sqlite")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute("""
SELECT name FROM sqlite_master
WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
""")

tables = [row[0] for row in cursor.fetchall()]

print("Таблицы базы данных:")
for table in tables:
    print(table)

assert len(tables) == 7, "Должно быть 7 таблиц"

try:
    cursor.execute("""
        INSERT INTO users (last_name, first_name, login, role_id)
        VALUES ('Иванов', 'Иван', 'test_user_123', 99999)
    """)
    print("ОШИБКА: внешний ключ не проверяется")
except sqlite3.IntegrityError as e:
    print("Проверка внешнего ключа пройдена:", e)

conn.rollback()
conn.close()
