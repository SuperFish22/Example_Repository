"""Утилиты работы с sqlite3: соединение, схема БД и демо‑сидирование.

Экспортируемые функции:
- get_db(): возвращает подключение sqlite3, привязанное к запросу
- close_db(): закрывает соединение после запроса
- init_db(): создаёт таблицы, если их нет
- seed_demo_data(): добавляет демо‑товары один раз
"""

import sqlite3
from flask import current_app, g

# SQL‑схема минимальной доменной модели магазина
SCHEMA = """
CREATE TABLE IF NOT EXISTS product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  price_cents INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS "order" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  total_cents INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS order_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER REFERENCES "order"(id),
  product_id INTEGER REFERENCES product(id),
  quantity INTEGER DEFAULT 1
);
"""


def get_db() -> sqlite3.Connection:
    """Получить подключение sqlite3, сохранённое в Flask `g` на время запроса.

    - Открывает соединение по пути из app.config['DATABASE_URL']
    - Устанавливает Row‑фабрику для доступа к колонкам по имени
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None) -> None:
    """Закрыть соединение, привязанное к текущему запросу, если оно есть."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Инициализировать схему БД выполнением DDL‑скриптов из SCHEMA."""
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


def seed_demo_data() -> None:
    """Добавить демо‑товары, если каталог пуст.

    Это упрощает первый запуск без ручного наполнения данных.
    """
    db = get_db()
    rows = db.execute('SELECT COUNT(*) as c FROM product').fetchone()
    if rows and rows['c'] == 0:
        db.executemany(
            'INSERT INTO product (sku, title, price_cents) VALUES (?, ?, ?)',
            [
                ('SKU-1', 'Футболка', 1990),
                ('SKU-2', 'Кепка', 1490),
                ('SKU-3', 'Кружка', 990),
            ],
        )
        db.commit()
