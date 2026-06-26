"""
Модуль для чтения финансовых транзакций из CSV и Excel файлов.
"""

import logging
import os
from typing import Any, Dict, List

import pandas as pd

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/file_reader.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые транзакции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если файл пустой или не содержит данных
        Exception: При других ошибках чтения
    """
    logger.info(f"Начало чтения CSV файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {file_path}")
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        df = pd.read_csv(file_path)

        if df.empty:
            logger.error("CSV файл пуст")
            raise ValueError("CSV файл пуст")

        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно прочитано {len(transactions)} транзакций из CSV")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при чтении CSV: {e}")
        raise


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые транзакции из Excel-файла.

    Args:
        file_path (str): Путь к Excel-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если файл пустой или не содержит данных
        Exception: При других ошибках чтения
    """
    logger.info(f"Начало чтения Excel файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {file_path}")
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        df = pd.read_excel(file_path)

        if df.empty:
            logger.error("Excel файл пуст")
            raise ValueError("Excel файл пуст")

        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно прочитано {len(transactions)} транзакций из Excel")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при чтении Excel: {e}")
        raise
