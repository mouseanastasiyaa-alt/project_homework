    # Модуль для функций виджета
from datetime import datetime
from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета с проверкой ввода."""
    if not info:
        return "Ошибка: пустая строка"

    parts = info.split()
    if len(parts) < 2:
        return "Ошибка: неверный формат (отсутствует номер или тип)"

    number = parts[-1]
    type_name = " ".join(parts[:-1])

    if "Счет" in type_name:
        return f"{type_name} {get_mask_account(number)}"
    else:
        return f"{type_name} {get_mask_card_number(number)}"

def get_date(date_str: str) -> str:
    """Превращает строку ISO в ДД.ММ.ГГГГ с помощью datetime."""
    try:
        # Преобразуем строку в объект даты
        date_obj = datetime.fromisoformat(date_str)
        # Возвращаем в нужном формате
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return "Ошибка: некорректный формат даты"

