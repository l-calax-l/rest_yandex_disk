# D6 — Полная валидация (Pydantic Data-классы)


## Что сделано

- TC-D6-01: Загрузка и копирование файла (TC-03 из задания)
- TC-D6-02: Скачивание текстового файла (TC-04 из задания)
- Исследование FrontEnd-запросов через DevTools
- Создание Pydantic Data-классов для сериализации/десериализации

## Что обнаружил
- Исследовал запросы Яндекс Диска и Полигона при создании/перемещении. 
- Сейчас используется внутреннее API [models-v2](image/devtools_disk_yandex.png), а не публичное [REST API](image/devtools_polygon.png).
<details>
  <summary><strong>Скриншот devtools Яндекс Диск (кликни, чтобы развернуть)</strong></summary>
  
  ![Скриншот с Яндекс Диска](image/devtools_disk_yandex.png)
</details>

<details>
  <summary><strong>Скриншот devtools Яндекс Полигон (кликни, чтобы развернуть)</strong></summary>
  
  ![Скриншот с Яндекс Полигона](/image/devtools_polygon.png)
</details>

## Data-классы (api/models/yandex_models.py)
```python
LinkResponse      — ответ с ссылкой (href, method, templated)
ErrorResponse     — ошибка API (error, message, description)
CopyResourceRequest — запрос на копирование (from_, path, overwrite)
LinkRequest       — запрос на получение ссылки (path, overwrite)