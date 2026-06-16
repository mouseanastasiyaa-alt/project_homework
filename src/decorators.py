import datetime
import functools
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор, автоматически регистрирующий детали выполнения функций.

    Логирует время вызова, имя функции, результат работы или ошибку с входными аргументами.
    Если filename задан — пишет лог в файл, если не задан — выводит в консоль.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                result = func(*args, **kwargs)
                log_message = f"{timestamp} {func.__name__} ok\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    sys.stdout.write(log_message)

                return result

            except Exception as e:
                # Если ошибка, пишем сообщение об ошибке и входные параметры
                log_message = f"{timestamp} {func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    sys.stdout.write(log_message)

                raise e

        return wrapper
    return decorator
