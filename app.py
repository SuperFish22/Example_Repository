"""Точка входа для запуска приложения локально.

Запуск (Windows PowerShell):
  python app.py
или
  $env:FLASK_APP = "app:create_app"; flask run --debug
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Встроенный dev-сервер Flask (для локальной разработки)
    app.run(debug=True)
