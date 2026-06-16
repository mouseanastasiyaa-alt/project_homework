import os
from typing import Any
import pytest
from src.decorators import log


@log()
def success_console_func(x: int, y: int) -> int:
    """Тестовая успешная функция для проверки консоли."""
    return x * y


@log()
def error_console_func() -> Any:
    """Тестовая функция с ошибкой для проверки консоли."""
    return 5 / 0


@log(filename="test_file_log.txt")
def success_file_func(name: str) -> str:
    """Тестовая функция для успешной записи в файл."""
    return f"Hello, {name}"


@pytest.mark.parametrize(
    "x, y, expected_result, expected_log",
    [
        (2, 3, 6, "success_console_func ok"),
        (10, 0, 0, "success_console_func ok"),
    ],
)
def test_log_success_console(
    capsys: pytest.CaptureFixture[str], x: int, y: int, expected_result: int, expected_log: str
) -> None:
    """Проверяем успешное логирование в консоль с помощью параметризации."""
    assert success_console_func(x, y) == expected_result
    captured = capsys.readouterr()
    assert expected_log in captured.out


def test_log_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяем запись сообщения об ошибке и входных параметров в консоль."""
    with pytest.raises(ZeroDivisionError):
        error_console_func()
    captured = capsys.readouterr()
    assert "error: ZeroDivisionError" in captured.out
    assert "Inputs:" in captured.out


def test_log_file_success() -> None:
    """Проверяем успешную запись лога выполнения функции в текстовый файл."""
    if os.path.exists("test_file_log.txt"):
        os.remove("test_file_log.txt")

    assert success_file_func("Python") == "Hello, Python"
    assert os.path.exists("test_file_log.txt")

    with open("test_file_log.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "success_file_func ok" in content

    os.remove("test_file_log.txt")


@log(filename="test_error_file.txt")
def error_file_func() -> Any:
    """Тестовая функция с ошибкой для проверки записи в файл."""
    return [][0]  # Вызовет IndexError


def test_log_error_file() -> None:
    """Проверяем запись сообщения об ошибке и входных параметров в файл."""
    if os.path.exists("test_error_file.txt"):
        os.remove("test_error_file.txt")

    with pytest.raises(IndexError):
        error_file_func()

    assert os.path.exists("test_error_file.txt")
    with open("test_error_file.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "error: IndexError" in content

    os.remove("test_error_file.txt")
