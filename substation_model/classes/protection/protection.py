"""
Модуль классов релейной защиты.
"""

import random


class Protection:
    """Базовый класс защиты."""

    def __init__(self, name_protected_equipment: str, setting: float,
                 vendor: str, base: str, failure_probability: float):
        self.__name_protected_equipment = name_protected_equipment
        self.__setting = setting
        self.__vendor = vendor
        self.__base = base
        self.__failure_probability = failure_probability
        self.__is_operational = True

    def get_protected_equipment(self) -> str:
        return self.__name_protected_equipment

    def get_setting(self) -> float:
        return self.__setting

    def get_failure_probability(self) -> float:
        return self.__failure_probability

    def check_fault(self, fault_current: float) -> bool:
        if not self.__is_operational:
            return False
        if random.random() < self.__failure_probability:
            self.__is_operational = False
            return False
        return fault_current > self.__setting

    def is_operational(self) -> bool:
        return self.__is_operational

    def reset(self):
        self.__is_operational = True

    def __str__(self) -> str:
        return f"Protection for {self.__name_protected_equipment} (setting: {self.__setting}A)"


class MainProtection(Protection):
    """Основная защита."""

    def __init__(self, name_protected_equipment: str, setting: float,
                 vendor: str, base: str, failure_probability: float):
        super().__init__(name_protected_equipment, setting, vendor, base, failure_probability)

    def get_type(self) -> str:
        return "Main"


class BackupProtection(Protection):
    """Резервная защита."""

    def __init__(self, name_protected_equipment: str, setting: float,
                 vendor: str, base: str, failure_probability: float):
        super().__init__(name_protected_equipment, setting, vendor, base, failure_probability)

    def get_type(self) -> str:
        return "Backup"