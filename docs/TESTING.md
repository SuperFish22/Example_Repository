# Тестирование

## Инструменты
- pytest
- Flask testing client

## Установка
```bash
pip install pytest pytest-cov
```

## Структура
```text
tests/
├── conftest.py
├── test_products.py
└── test_checkout.py
```

## Пример conftest.py
```python
import os
import tempfile
import pytest
from app import create_app

@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config.update({
        'TESTING': True,
        'DATABASE_URL': db_path,
    })
    with app.app_context():
        from app.db import init_db
        init_db()
    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture()
def client(app):
    return app.test_client()
```

## Примеры тестов
```python
# tests/test_products.py

def test_products_list_page(client):
    resp = client.get('/')
    assert resp.status_code == 200

# tests/test_checkout.py

def test_checkout_missing_sku(client):
    resp = client.get('/checkout')
    assert resp.status_code in (302, 400, 404)
```

## Запуск тестов
```bash
pytest -q --cov=app
```
