# D7 — JSON Schema Validation


## Что сделано
- TC-D7-01: Валидация ответа GET /resources по JSON Schema
- Создана JSON Schema для метаинформации о ресурсе
- Схема покрывает: name, path, type, created, modified, _embedded

## JSON Schema (schemas/resource_info_schema.json)
- Проверяет обязательные поля: name, path, type, created, modified
- Проверяет типы данных всех полей
- Проверяет вложенную структуру _embedded.items
- `additionalProperties: false` — строгая валидация
