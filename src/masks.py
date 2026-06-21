"""
Модуль для маскировки номеров карт и счетов.
"""

import logging
import os

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Формат маски: "XXXX XX** **** XXXX"

    Args:
        card_number (str): Номер карты в виде строки (16 цифр)

    Returns:
        str: Замаскированный номер карты

    Example:
        >>> get_mask_card_number("1234567890123456")
        '1234 56** **** 3456'
    """
    if not card_number:
        return " ** **** "
    # Очищаем от пробелов
    clean = card_number.replace(" ", "")
    if len(clean) >= 16:
        return f"{clean[:4]} {clean[4:6]}** **** {clean[-4:]}"
    return card_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета.

    Формат маски: "**XXXX", где XXXX - последние 4 цифры счета.
    Если номер короткий (менее 4 цифр), возвращает "**" + номер.

    Args:
        account_number (str): Номер счета в виде строки

    Returns:
        str: Замаскированный номер счета

    Example:
        >>> get_mask_account("1234567890123456")
        '**3456'
        >>> get_mask_account("123")
        '**123'
    """
    logger.info(f"Начало маскирования номера счета: {account_number[:4]}****")

    if not account_number:
        logger.warning("Получен пустой номер счета")
        return "**"

    # Извлекаем только цифры
    digits_only = "".join(filter(str.isdigit, account_number))

    if len(digits_only) < 4:
        logger.warning(f"Номер счета слишком короткий: {digits_only}")
        return f"**{digits_only}" if digits_only else "**"

    logger.info(f"Номер счета замаскирован: **{digits_only[-4:]}")
    return f"**{digits_only[-4:]}"