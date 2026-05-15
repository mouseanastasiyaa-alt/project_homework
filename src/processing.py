from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_list = []
    for item in data:
        if item.get("state") == state:
            filtered_list.append(item)
    return filtered_list


def sort_by_date(data: List[Dict[str, Any]], sort_order: str = "True") -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'."""
    is_reverse = sort_order == "True"
    return sorted(data, key=lambda item: item.get("date", ""), reverse=is_reverse)
