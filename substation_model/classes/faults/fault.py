"""
Модуль классов повреждений
"""

from abc import ABC, abstractmethod
import random


class Fault(ABC):
    """Абстрактный базовый класс повреждения."""
    #нельзя создать экземпляр класса
    #обеспечивается единство интерфейсов дочерних классов

    def __init__(self, fault_type: str, voltage: str):
        self.__fault_type = fault_type
        self.__voltage = voltage
        self.__fault_current = 0.0
        self.__is_self_cleared = False

    @abstractmethod  # Декоратор объявляет метод абстрактным — дочерние классы обязаны его реализовать
    def calculate_fault_current(self) -> float:
        pass

    def get_fault_type(self) -> str:
        return self.__fault_type

    def get_voltage(self) -> str:
        return self.__voltage

    def get_fault_current(self) -> float:
        return self.__fault_current

    def set_fault_current(self, current: float):
        self.__fault_current = current

    def is_self_cleared(self) -> bool:
        return self.__is_self_cleared

    def set_self_cleared(self, status: bool):
        self.__is_self_cleared
        status

    def __str__(self) -> str:
        return f"{self.__fault_type} ({self.__voltage}): {self.__fault_current:.2f} A"


class ThreePhaseFault(Fault):
    """Трёхфазное КЗ."""

    def __init__(self, voltage: str):
        super().__init__("ThreePhase", voltage)

    def calculate_fault_current(self) -> float:
        base_current = 300 if "110" in self.get_voltage() else 2200
        self.set_fault_current(random.uniform(base_current * 1.5, base_current * 3.0))
        return self.get_fault_current()


class TwoPhaseFault(Fault):
    """Двухфазное КЗ."""

    def __init__(self, voltage: str):
        super().__init__("TwoPhase", voltage)

    def calculate_fault_current(self) -> float:
        base_current = 300 if "110" in self.get_voltage() else 2200
        self.set_fault_current(random.uniform(base_current * 0.8, base_current * 1.5))
        return self.get_fault_current()


class SinglePhaseFault(Fault):
    """Однофазное КЗ."""

    def __init__(self, voltage: str):
        super().__init__("SinglePhase", voltage)

    def calculate_fault_current(self) -> float:
        base_current = 300 if "110" in self.get_voltage() else 2200
        self.set_fault_current(random.uniform(base_current * 0.7, base_current * 1.2))
        return self.get_fault_current()


class TurnToTurnFault(Fault):
    """Межвитковое КЗ в трансформаторе"""

    def __init__(self, voltage: str):
        super().__init__("TurnToTurn", voltage)

    def calculate_fault_current(self) -> float:
        base_current = 400 if "110" in self.get_voltage() else 800
        self.set_fault_current(random.uniform(base_current * 0.6, base_current * 1.3))
        return self.get_fault_current()


class FaultFactory:
    """Создатель повреждений."""

    @staticmethod  # Декоратор делает метод статическим — можно вызывать без создания экземпляра класса
    def create_fault(fault_type: str, voltage: str) -> Fault:
        fault_map = {
            "ThreePhase": ThreePhaseFault,
            "TwoPhase": TwoPhaseFault,
            "SinglePhase": SinglePhaseFault,
            "TurnToTurn": TurnToTurnFault
        }
        fault_class = fault_map.get(fault_type, ThreePhaseFault)
        return fault_class(voltage)

    @staticmethod  # Декоратор делает метод статическим — можно вызывать без создания экземпляра класса
    def get_random_fault_type(equipment_type: str) -> str:
        if equipment_type == "Transformer":
            return random.choice(["ThreePhase", "TwoPhase", "SinglePhase", "TurnToTurn"])
        return random.choice(["ThreePhase", "TwoPhase", "SinglePhase"])