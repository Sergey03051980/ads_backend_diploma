## 1. Регистрация пользователя
```bash
curl -X POST http://localhost:8001/api/user/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "DemoPass123",
    "first_name": "Demo",
    "last_name": "User", 
    "phone": "+79991234567"
  }'
2. Получение JWT токена
bash
curl -X POST http://localhost:8001/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "DemoPass123"
  }'
3. Получение списка объявлений
bash
curl http://localhost:8001/api/ads/
4. Поиск объявлений
bash
curl "http://localhost:8001/api/ads/?search=ноутбук"
5. Создание объявления
bash
curl -X POST http://localhost:8001/api/ads/create/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ноутбук Dell",
    "price": 150000,
    "description": "Мощный ноутбук для работы"
  }'
6. Комментарии к объявлению
bash
# Список комментариев
curl http://localhost:8001/api/ads/1/comments/

# Создание комментария
curl -X POST http://localhost:8001/api/ads/1/comments/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Отличное объявление!"}'
