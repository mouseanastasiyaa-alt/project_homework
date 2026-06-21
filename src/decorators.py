"""
Модуль с декораторами для логирования выполнения функций.
"""

import functools
import os
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename (Optional[str]): Имя файла для записи логов.
                                  Если не указан, логи выводятся в консоль.

    Returns:
        Callable: Декорированная функция

    Example:
        >>> @log()
        >>> def my_func(x, y):
        >>>     return x + y
        >>>
        >>> @log(filename="mylog.txt")
        >>> def another_func(data):
        >>>     return data.upper()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                if filename:
                    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{func.__name__} ok\n")
                else:
                    print(f"{func.__name__} ok")
                return result
            except Exception as e:
                if filename:
                    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n")
                else:
                    print(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise
        return wrapper
    return decorator
