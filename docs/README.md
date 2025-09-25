# Документация: Flask + sqlite3 Интернет‑магазин (прямое оформление заказа)

Добро пожаловать в документацию будущего проекта. Это минималистичный интернет‑магазин на Flask со встроенным модулем `sqlite3`, где вместо добавления в корзину пользователь сразу переходит на форму оформления заказа.

## Оглавление
- Архитектура: `ARCHITECTURE.md`
- Установка и запуск: `SETUP.md`
- API спецификация: `API.md`
- Деплой: `DEPLOYMENT.md`
- Тестирование: `TESTING.md`
- Стиль кода: `STYLE_GUIDE.md`
- Контрибьютинг: `CONTRIBUTING.md`
- FAQ: `FAQ.md`

## Кратко о проекте
- Backend: Flask (Python 3.10+)
- База данных: sqlite3 (стандартная библиотека)
- Шаблоны: Jinja2
- Особенность: кнопка «Купить» ведет на форму оформления заказа, минуя корзину

## Быстрый старт
См. подробности в `SETUP.md`. Вкратце:
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app run --debug
```


