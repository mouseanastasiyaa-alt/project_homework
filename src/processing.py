def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список словарей по значению ключа 'state'.

    Возвращает новый список, содержащий только те словари, у которых
    ключ state соответствует переданному значению (по умолчанию 'EXECUTED').
    """
    filtered_list = []
    for item in data:
        if item.get("state") == state:
            filtered_list.append(item)
    return filtered_list


def sort_by_date(data: list[dict], is_descending: bool = True) -> list[dict]:
    """Сортирует список словарей по ключу 'date'.

    Принимает логический параметр порядка сортировки (по умолчанию True — убывание).
    Возвращает новый отсортированный список.
    """
    return sorted(data, key=lambda item: item.get("date", ""), reverse=is_descending)
