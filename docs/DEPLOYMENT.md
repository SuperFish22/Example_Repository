# Деплой

## Среды
- dev: отладка включена, файл SQLite в репозитории
- prod: отладка выключена, файл SQLite вне репозитория (или внешняя БД)

## Переменные окружения
- `FLASK_ENV` = production | development
- `DATABASE_URL` = путь к файлу SQLite (напр. `C:/data/shop.db`)
- `SECRET_KEY` = сильный случайный ключ

## Запуск в продакшене (пример)
1. Создайте виртуальное окружение и установите зависимости
2. Экспортируйте переменные окружения
3. Запустите через WSGI‑сервер (gunicorn/Waitress) позади реверс‑прокси (Nginx/IIS)

### Пример (Waitress на Windows)
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install waitress flask python-dotenv
$env:FLASK_ENV = "production"
$env:DATABASE_URL = "C:/data/shop.db"
$env:SECRET_KEY = "<generate-strong-key>"
python -c "from app import create_app; from waitress import serve; serve(create_app(), host='0.0.0.0', port=8080)"
```

## Статические файлы
- Обслуживайте через веб‑сервер (Nginx/IIS) или Flask `send_from_directory`

## Миграции
- Для sqlite3 используйте `executescript` со схемой; при росте — перенос на миграции (Alembic при переходе на SQLAlchemy или собственные скрипты)
