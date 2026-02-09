import time
from typing import Any, Callable

from config import settings


def wait_for_result(
    func: Callable[[], Any],
    timeout: int = settings.time_out,
    poll_interval: float = settings.poll_interval,
    error_message: str = "Результат не получен за время таймаута",
) -> Any:
    """
    Ждет, пока func() вернет значение (не None, не False, не пустой список).
    Возвращает это значение.
    """
    start_time = time.time()
    last_exception = None

    while time.time() - start_time < timeout:
        try:
            result = func()
            if result:
                return result
        except Exception as e:
            last_exception = e

        time.sleep(poll_interval)

    raise TimeoutError(f"{error_message}. Последняя ошибка: {last_exception}")
