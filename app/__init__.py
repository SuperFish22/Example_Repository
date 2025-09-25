"""Фабрика Flask‑приложения для демо‑магазина на sqlite3.

Этот модуль предоставляет функцию `create_app`, которая настраивает Flask‑приложение,
регистрирует blueprints и инициализирует схему базы данных при старте.
"""

from flask import Flask
import os


def create_app() -> Flask:
    """Создать и настроить экземпляр Flask‑приложения.

    - Читает DATABASE_URL из окружения (по умолчанию 'app.db')
    - Регистрирует основной веб‑blueprint
    - Инициализирует схему БД при запуске приложения
    """
    app = Flask(__name__)
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'app.db')

    from .routes import bp as web_bp
    app.register_blueprint(web_bp)

    from .db import init_db
    with app.app_context():
        init_db()

    return app
