"""Веб‑маршруты и JSON API для демо‑магазина.

Страницы:
- /             : список товаров
- /product/<sku>: карточка товара
- /checkout     : оформление заказа (GET/POST)
- /order/<id>   : подтверждение заказа

API:
- GET  /api/products
- POST /api/orders
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from .db import get_db, seed_demo_data
from .services.orders import create_order, get_order

bp = Blueprint('web', __name__)


@bp.before_app_request
def ensure_seed():
    """Заполнить демо‑каталог при первом запросе, если БД пуста."""
    seed_demo_data()


@bp.route('/')
def index():
    """Список товаров со ссылками на карточку и прямую покупку."""
    db = get_db()
    products = db.execute('SELECT * FROM product ORDER BY id').fetchall()
    return render_template('index.html', products=products)


@bp.route('/product/<sku>')
def product_page(sku):
    """Карточка товара по SKU."""
    db = get_db()
    product = db.execute('SELECT * FROM product WHERE sku = ?', (sku,)).fetchone()
    if product is None:
        abort(404)
    return render_template('product.html', product=product)


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Поток прямого оформления заказа.

    GET ожидает параметр `sku` в query; POST — поля формы: sku, email, quantity.
    """
    if request.method == 'GET':
        sku = request.args.get('sku')
        if not sku:
            abort(400)
        db = get_db()
        product = db.execute('SELECT * FROM product WHERE sku = ?', (sku,)).fetchone()
        if product is None:
            abort(404)
        return render_template('checkout.html', product=product)

    # POST
    sku = request.form.get('sku')
    email = request.form.get('email')
    quantity = int(request.form.get('quantity') or 1)
    if not sku or not email:
        abort(400)
    order_id = create_order(email=email, sku=sku, quantity=quantity)
    if order_id is None:
        abort(404)
    return redirect(url_for('web.order_success', order_id=order_id))


@bp.route('/order/<int:order_id>')
def order_success(order_id):
    """Страница подтверждения заказа с кратким итогом заказа."""
    order, items = get_order(order_id)
    if order is None:
        abort(404)
    return render_template('order.html', order=order, items=items)


# JSON API
@bp.route('/api/products')
def api_products():
    """Вернуть список товаров в формате JSON."""
    db = get_db()
    products = db.execute('SELECT id, sku, title, price_cents FROM product ORDER BY id').fetchall()
    return jsonify([dict(p) for p in products])


@bp.route('/api/orders', methods=['POST'])
def api_create_order():
    """Создать заказ из JSON‑тела: { email, items: [{ sku, quantity }] }"""
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    items = data.get('items') or []
    if not email or not items:
        return jsonify({'error': 'email and items are required'}), 400
    first = items[0]
    sku = first.get('sku')
    quantity = int(first.get('quantity') or 1)
    order_id = create_order(email=email, sku=sku, quantity=quantity)
    if order_id is None:
        return jsonify({'error': 'SKU not found'}), 404
    return jsonify({'id': order_id}), 201
