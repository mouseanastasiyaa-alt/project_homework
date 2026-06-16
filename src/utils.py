import json
import logging
import os
from typing import Any

# 1. Создаем объект логера для модуля utils и ставим уровень DEBUG
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# На всякий случай проверяем и создаем папку logs
os.makedirs("logs", exist_ok=True)

# 2. Настраиваем file_handler с перезаписью файла (mode="w")
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")

# 3. Настраиваем file_formatter
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 4. Устанавливаем форматер и добавляем handler к логеру
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_financial_data(file_path: str) -> list[dict[str, Any]]:

    """Открывает JSON-файл и возвращает список транзакций."""
    logger.info(f"Попытка открыть файл транзакций по пути: {file_path}")

    # Логирование ошибочного случая: файл отсутствует
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден по указанному пути: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Логирование ошибочного случая: данные внутри файла не список
        if not isinstance(data, list):
            logger.error(f"Данные в файле {file_path} не являются списком JSON")
            return []

        # Логирование успешного случая использования
        logger.info(f"Файл {file_path} успешно прочитан. Найдено транзакций: {len(data)}")
        return data

    except json.JSONDecodeError as e:
        # Логирование ошибочного случая: поврежденная структура JSON
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
