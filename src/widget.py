"""
Модуль для работы с виджетами и форматированием данных.

Содержит функции для форматирования и отображения финансовой информации.
"""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Args:
        card_or_account (str): Строка с типом и номером карты/счета.
                              Например: "Visa Platinum 1234567890123456"
                                       или "Счет 1234567890123456"

    Returns:
        str: Строка с замаскированным номером.

    Example:
        >>> mask_account_card("Visa Platinum 1234567890123456")
        'Visa Platinum 1234 56** **** 3456'
        >>> mask_account_card("Счет 1234567890123456")
        'Счет **3456'
    """
    # Разделяем на тип и номер
    parts = card_or_account.rsplit(" ", 1)

    if len(parts) != 2:
        return card_or_account

    card_type, number = parts[0], parts[1]

    # Проверяем, содержит ли номер только цифры и его длину
    clean_number = number.replace(" ", "")

    if len(clean_number) == 16 and clean_number.isdigit():
        # Это карта
        masked_number = get_mask_card_number(clean_number)
        return f"{card_type} {masked_number}"
    else:
        # Это счет
        masked_number = get_mask_account(clean_number)
        return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string (str): Дата в формате "YYYY-MM-DDTHH:MM:SS.MS"

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ"

    Example:
        >>> get_date("2024-01-15T10:30:00.123")
        '15.01.2024'
    """
    if not date_string:
        return ""

    # Извлекаем только дату (до T)
    date_part = date_string.split("T")[0]
    year, month, day = date_part.split("-")

    return f"{day}.{month}.{year}"
