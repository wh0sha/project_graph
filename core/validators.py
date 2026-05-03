# core/validators.py
"""Утилиты для безопасного парсинга и базовой валидации пользовательского ввода."""
import re
from typing import List, Dict, Tuple, Union, Optional

def parse_sequence(text: str) -> Optional[List[int]]:
    """Парсит строку вида '0, 1, 2, 3' → [0, 1, 2, 3]. Возвращает None при ошибке."""
    try:
        return [int(x.strip()) for x in text.split(',') if x.strip()]
    except ValueError:
        return None

def parse_components(text: str) -> Optional[List[List[int]]]:
    """Парсит строку вида '[0,1], [2,3]' → [[0, 1], [2, 3]]. Возвращает None при ошибке."""
    try:
        raw = text.strip().strip('[]')
        if not raw:
            return []
        # Разделяем по '],[' или просто по запятым между скобками
        groups = re.findall(r'\[([^\]]+)\]', text)
        if not groups:
            # Пробуем формат без скобок: 0,1, 2,3
            groups = [g.strip() for g in re.split(r',\s*', raw) if g.strip()]
        result = []
        for g in groups:
            nums = [int(x.strip()) for x in g.replace('[', '').replace(']', '').split(',') if x.strip()]
            if nums:
                result.append(nums)
        return result
    except ValueError:
        return None

def parse_edges(text: str) -> Optional[List[Tuple[int, int]]]:
    """Парсит строку вида '(0,1), (1,2)' → [(0,1), (1,2)]. Возвращает None при ошибке."""
    try:
        matches = re.findall(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)', text)
        return [(int(u), int(v)) for u, v in matches]
    except Exception:
        return None

def parse_colors(text: str) -> Optional[Dict[int, int]]:
    """Парсит строку вида '1, 2, 1, 2, 3' → {0:1, 1:2, 2:1, 3:2, 4:3}. Возвращает None при ошибке."""
    try:
        vals = [int(x.strip()) for x in text.split(',') if x.strip()]
        return {i: c for i, c in enumerate(vals)}
    except ValueError:
        return None

def validate_not_empty(value: any, field_name: str = "Поле") -> Dict:
    """Базовая проверка на пустоту/None."""
    if value is None:
        return {"correct": False, "feedback": f"{field_name} не заполнено или имеет неверный формат"}
    if isinstance(value, list) and len(value) == 0:
        return {"correct": False, "feedback": f"{field_name} пустое. Введите данные."}
    return {"correct": True}