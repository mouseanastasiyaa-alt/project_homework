from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """Определяет тип карты или счета и применяет маскировку."""
    if not input_string:
        return ""

    parts = input_string.split()
    number = parts[-1]
    type_name = " ".join(parts[:-1])

    if "Счет" in type_name:
        return f"{type_name} {get_mask_account(number)}"
    return f"{type_name} {get_mask_card_number(number)}"


def get_date(date_string: str) -> str:
    """Преобразует строку с датой в формат ДД.ММ.ГГГГ."""
    if not date_string or len(date_string) < 10:
        return ""
    date_part = date_string[:10]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
