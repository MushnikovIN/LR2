"""
Генерация случайных событий
"""

import random


def select_random_equipment(equipment_dict: dict) -> tuple:
    if not equipment_dict:
        return None, None
    name = random.choice(list(equipment_dict.keys()))
    return name, equipment_dict[name]