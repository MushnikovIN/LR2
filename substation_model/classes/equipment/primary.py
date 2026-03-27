"""
Модуль основного оборудования подстанции.
"""

from abc import ABC, abstractmethod


class PrimaryEquipment(ABC):
    """Абстрактный базовый класс первичного оборудования."""

    def __init__(self, name: str, voltage: str):
        self.__name = name
        self.__voltage = voltage
        self.__is_operational = True

    @abstractmethod  # Декоратор объявляет метод абстрактным — дочерние классы обязаны его реализовать
    def get_type(self) -> str:
        pass

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_voltage(self) -> str:
        return self.__voltage

    def set_voltage(self, voltage: str):
        self.__voltage = voltage

    def is_operational(self) -> bool:
        return self.__is_operational

    def set_operational(self, status: bool):
        self.__is_operational = status

    def __str__(self) -> str:
        return f"{self.get_type()} {self.__name} ({self.__voltage})"


class Bus(PrimaryEquipment):
    """Класс шины"""

    def __init__(self, name: str, voltage: str, section: int, switched_by: list):
        super().__init__(name, voltage)
        self.__section = section
        self.__switched_by = switched_by

    def get_type(self) -> str:
        return "Bus"

    def get_section(self) -> int:
        return self.__section

    def set_section(self, section: int):
        self.__section = section

    def get_switched_by(self) -> list:
        return self.__switched_by.copy()


class Line(PrimaryEquipment):
    """Класс линии электропередачи"""

    def __init__(self, name: str, voltage: str, connected_with: list, switched_by: list):
        super().__init__(name, voltage)
        self.__connected_with = connected_with
        self.__switched_by = switched_by

    def get_type(self) -> str:
        return "Line"

    def get_connected_with(self) -> list:
        return self.__connected_with.copy()

    def get_switched_by(self) -> list:
        return self.__switched_by.copy()


class Transformer(PrimaryEquipment):
    """Класс силового трансформатора"""

    def __init__(self, name: str, voltage: str, power: int, hv: int, lv: int, connected_with: list, switched_by: list):
        super().__init__(name, voltage)
        self.__power = power
        self.__hv = hv
        self.__lv = lv
        self.__connected_with = connected_with
        self.__switched_by = switched_by

    def get_type(self) -> str:
        return "Transformer"

    def get_power(self) -> int:
        return self.__power

    def set_power(self, power: int):
        self.__power = power

    def get_hv(self) -> int:
        return self.__hv

    def get_lv(self) -> int:
        return self.__lv

    def get_connected_with(self) -> list:
        return self.__connected_with.copy()

    def get_switched_by(self) -> list:
        return self.__switched_by.copy()


class CircuitBreaker(PrimaryEquipment):
    """Класс выключателя"""

    def __init__(self, name: str, voltage: str, normal_state: str):
        super().__init__(name, voltage)
        self.__state = normal_state
        self.__normal_state = normal_state

    def get_type(self) -> str:
        return "CircuitBreaker"

    def get_state(self) -> str:
        return self.__state

    def set_state(self, state: str):
        if state in ["closed", "open"]:
            self.__state = state

    def switch_on(self):
        self.__state = "closed"

    def switch_off(self):
        self.__state = "open"

    def is_closed(self) -> bool:
        return self.__state == "closed"

    def reset_to_normal(self):
        self.__state = self.__normal_state