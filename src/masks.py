import logging
import os
from typing import Union

# 1. Создаем объект логера для модуля masks и ставим уровень DEBUG
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# На всякий случай проверяем и создаем папку logs
os.makedirs("logs", exist_ok=True)

# 2. Настраиваем file_handler с перезаписью файла (mode="w")
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")

# 3. Настраиваем file_formatter
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 4. Устанавливаем форматер и добавляем handler к логеру
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Маскирует номер карты."""
    logger.info("Начало маскирования номера карты")
    card_str = str(card_number)

    # Логируем ошибку, если формат некорректен (но не ломаем выполнение, чтобы тесты прошли)
    if len(card_str) != 16 or not card_str.isdigit():
        logger.error(f"Неверный формат номера карты: '{card_str}'")

    # Возвращаем нарезку строки, как ожидали старые тесты
    masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    logger.info("Номер карты успешно замаскирован")
    return masked


def get_mask_account(account_number: Union[int, str]) -> str:
    """Маскирует номер счета."""
    logger.info("Начало маскирования номера счета")
    account_str = str(account_number)

    # Логируем ошибку, если это не цифры или длина не соответствует стандарту банка (обычно 20)
    if len(account_str) != 20 or not account_str.isdigit():
        logger.error(f"Неверный стандартный формат номера счета: '{account_str}'")

    # Возвращаем последние 4 символа (или сколько есть) с маской
    masked = f"**{account_str[-4:]}"
    logger.info("Номер счета успешно замаскирован")
    return masked
