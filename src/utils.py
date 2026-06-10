import json
from pathlib import Path
from typing import Any


def read_json_file(file_path: str) -> list[dict[str, Any]]:
    """Читает JSON-файл с финансовыми транзакциями.

    Возвращает список словарей. Если файл пустой, содержит не-список
    или не найден, возвращает пустой список.
    """
    # Безопасная проверка: передан ли путь и существует ли файл физически
    if not file_path or not Path(file_path).is_file():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Проверяем критерий: "содержит не-список" (например, словарь или строку)
            if isinstance(data, list):
                return data
            return []

    # Ловим ошибку, если JSON пустой или поврежден
    except (json.JSONDecodeError, ValueError):
        return []

