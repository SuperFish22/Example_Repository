# Установка и запуск (Flask + sqlite3)

## Предпосылки
- Python 3.10+
- Windows: PowerShell

## Локальный запуск
```bash
python -m venv .venv
. .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
pip install -U pip
pip install flask pydantic python-dotenv
```

Создайте структуру проекта (минимум):
```text
app/
├── __init__.py
├── db.py
├── routes.py
├── services/
│   └── orders.py
└── templates/
    ├── index.html
    └── checkout.html
```

Минимальный `app/__init__.py`:
```python
from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'app.db')

    from .routes import bp as web_bp
    app.register_blueprint(web_bp)

    from .db import init_db
    with app.app_context():
        init_db()

    return app
```

Простой `app/db.py`:
```python
import sqlite3
from flask import current_app, g

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

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()
```

Запуск:
```bash
$env:FLASK_APP = "app:create_app"
$env:FLASK_ENV = "development"
flask run --debug
```

## Переменные окружения
- `DATABASE_URL` — путь к файлу SQLite (по умолчанию `app.db`)
- `SECRET_KEY` — секрет для сессий (установите в .env при необходимости)

## Разрешение проблем
- sqlite lock: закройте конкурирующие процессы или включите WAL (`PRAGMA journal_mode=WAL;`).
- Проблемы с импортом: активируйте виртуальное окружение.
