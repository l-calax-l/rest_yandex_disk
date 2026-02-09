import json
import os

import allure
from jsonschema import ValidationError, validate


def validate_schema(response_json: dict, schema_name: str):
    """
    Валидирует JSON ответа по схеме из папки schemas/
    """
    schema_path = os.path.join("schemas", schema_name)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        allure.attach(
            str(e), name="Validation Error", attachment_type=allure.attachment_type.TEXT
        )
        raise AssertionError(f"Ошибка валидации JSON Schema: {e.message}")
