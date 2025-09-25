# Архитектура

## Обзор
Простой интернет‑магазин с прямым оформлением заказа:
- Каталог товаров (листинг, карточка)
- Кнопка «Купить» ведет на `checkout` с выбранным SKU
- Оформление и сохранение заказа без корзины

## Компоненты
```text
app/
├── __init__.py         # фабрика приложения
├── db.py               # подключение к sqlite3, схемы
├── routes.py           # веб‑роуты и контроллеры
├── services/
│   └── orders.py       # бизнес‑логика оформления заказа
└── templates/          # Jinja2 шаблоны
```

## Схема БД (sqlite3)
```sql
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
```

## Потоки
1. Пользователь открывает `/` → видит товары
2. Нажимает «Купить» → редирект на `/checkout?sku=...`
3. Заполняет форму → POST `/checkout` → создаются записи в `order` и `order_item`
4. Страница подтверждения заказа

## Ошибки и валидация
- SKU не найден → 404
- Неверные поля формы → 400 с сообщениями и повторным рендером шаблона
