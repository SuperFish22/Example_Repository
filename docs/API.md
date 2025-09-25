# API спецификация

## Публичные страницы (HTML)
- `GET /` — листинг товаров
- `GET /product/<sku>` — страница товара
- `GET /checkout?sku=<sku>` — форма оформления заказа
- `POST /checkout` — оформить заказ, затем редирект на `/order/<id>`
- `GET /order/<id>` — страница подтверждения заказа

## JSON API (минимум)
- `GET /api/products` — список товаров
  - Ответ 200:
  ```json
  [{"id":1,"sku":"SKU-1","title":"Товар","price_cents":9900}]
  ```
- `POST /api/orders` — оформить заказ
  - Тело:
  ```json
  {"email":"user@example.com","items":[{"sku":"SKU-1","quantity":1}]}
  ```
  - Ответ 201:
  ```json
  {"id":123,"total_cents":9900}
  ```
  - Ошибки: 400 (валидация), 404 (SKU)

## Статусы и ошибки
- 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error
- Ошибки возвращаются как JSON { "error": "message" } в API
