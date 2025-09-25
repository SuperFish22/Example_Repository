"""Сервис заказов: инкапсулирует бизнес‑логику оформления и получения заказов.

Функции:
- find_product_by_sku(sku): вернуть строку товара или None
- create_order(email, sku, quantity): создать заказ и вернуть id или None
- get_order(order_id): вернуть (строка заказа, список строк позиций)
"""

from flask import current_app
from ..db import get_db


def find_product_by_sku(sku: str):
    """Найти товар по SKU. Возвращает sqlite3.Row или None."""
    db = get_db()
    row = db.execute('SELECT * FROM product WHERE sku = ?', (sku,)).fetchone()
    return row


def create_order(email: str, sku: str, quantity: int = 1):
    """Создать новый заказ с одной позицией по заданному SKU.

    Считает итог как price_cents * quantity.
    Возвращает id созданного заказа или None, если SKU не существует.
    """
    db = get_db()
    product = find_product_by_sku(sku)
    if product is None:
        return None
    total = int(product['price_cents']) * int(quantity)
    cur = db.execute('INSERT INTO "order" (email, total_cents) VALUES (?, ?)', (email, total))
    order_id = cur.lastrowid
    db.execute(
        'INSERT INTO order_item (order_id, product_id, quantity) VALUES (?, ?, ?)',
        (order_id, product['id'], quantity),
    )
    db.commit()
    return order_id


def get_order(order_id: int):
    """Вернуть строку заказа и связанные позиции с полями товара.

    Возвращает кортеж: (строка заказа или None, список строк позиций).
    """
    db = get_db()
    order = db.execute('SELECT * FROM "order" WHERE id = ?', (order_id,)).fetchone()
    items = db.execute(
        'SELECT oi.*, p.sku, p.title, p.price_cents FROM order_item oi JOIN product p ON p.id = oi.product_id WHERE oi.order_id = ?',
        (order_id,),
    ).fetchall()
    return order, items
