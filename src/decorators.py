"""
Модуль с декораторами для логирования выполнения функций.

Содержит декоратор @log для автоматического логирования вызовов функций
в консоль или файл.
"""

import functools
import logging
import os
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename (Optional[str]): Имя файла для записи логов.
                                  Если не указан, логи выводятся в консоль.
                                  Если указан, логи сохраняются в файл.

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
        """
        Внутренний декоратор, который оборачивает функцию.

        Args:
            func (Callable): Функция для декорирования

        Returns:
            Callable: Обернутая функция
        """
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Обертка функции, выполняющая логирование.

            Args:
                *args: Позиционные аргументы функции
                **kwargs: Именованные аргументы функции

            Returns:
                Any: Результат выполнения функции
            """
            if filename:
                # Логирование в файл
                os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
                logging.basicConfig(
                    filename=filename,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                )
                logger = logging.getLogger(__name__)
                logger.info(f"Вызов функции {func.__name__} с аргументами {args} {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"Функция {func.__name__} вернула {result}")
                return result
            else:
                # Логирование в консоль
                print(f"Вызов функции {func.__name__} с аргументами {args} {kwargs}")
                result = func(*args, **kwargs)
                print(f"Функция {func.__name__} вернула {result}")
                return result
        return wrapper
    return decorator