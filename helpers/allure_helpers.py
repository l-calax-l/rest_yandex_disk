import json
from typing import Any, Optional, Union

import allure


def attach_api_response(
    response,
    expected_status: Union[int, list[int], None] = None,
    name: str = "API Response",
) -> None:
    """Прикрепляет детали API ответа к Allure отчёту."""

    details = [f"Status Code: {response.status_code}"]

    if expected_status is not None:
        if isinstance(expected_status, list):
            is_match = response.status_code in expected_status
        else:
            is_match = response.status_code == expected_status

        status_match = "MATCH" if is_match else "MISMATCH"
        details.append(f"Expected: {expected_status} ({status_match})")

    try:
        response_json = response.json()

        error_code = (
            response_json.get("error")
            or response_json.get("error_code")
            or response_json.get("code")
        )

        if error_code:
            details.append(f"Error Code: {error_code}")

        formatted_body = json.dumps(response_json, indent=4, ensure_ascii=False)
        details.append(f"\nResponse Body (JSON):\n{formatted_body}")

    except ValueError:
        text_body = response.text[:1000]
        details.append(f"\nResponse Body (Text):\n{text_body}")

    final_content = "\n".join(details)
    allure.attach(final_content, name=name, attachment_type=allure.attachment_type.TEXT)


def attach_validation_result(
    field: str,
    expected: Any,
    actual: Any,
    passed: Optional[bool] = None,
    name: Optional[str] = None,
) -> None:
    """Прикрепляет результат валидации поля к Allure отчёту."""
    if passed is None:
        passed = expected in actual

    status = "PASSED" if passed else "FAILED"

    details = f"Expected: {expected}\n" f"Actual: {actual}\n" f"\nValidation: {status}"

    if name is None:
        name = f"Validation: {field}"

    allure.attach(details, name=name, attachment_type=allure.attachment_type.TEXT)
