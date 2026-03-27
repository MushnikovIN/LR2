"""
Класс подстанции. Управляет всем оборудованием и защитами.
"""

import json
from classes.equipment.primary import Bus, Line, Transformer, CircuitBreaker
from classes.faults.fault import FaultFactory, Fault
from classes.protection.protection import MainProtection, BackupProtection


class Substation:
    """Класс подстанции."""

    def __init__(self, config_path: str):
        self.__name = ""
        self.__buses = {}
        self.__lines = {}
        self.__transformers = {}
        self.__circuit_breakers = {}
        self.__protections = {}
        self.__load_config(config_path)

    def __load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            #print(config)

        substation = config['substation']
        self.__name = substation['name']

        for bus_data in substation['buses']:
            bus = Bus(bus_data['name'], bus_data['voltage'], bus_data['section'], bus_data.get('switched_by', []))
            self.__buses[bus.get_name()] = bus

        for line_data in substation['lines']:
            line = Line(
                line_data['name'],
                line_data['voltage'],
                line_data['connected_with'],
                line_data['switched_by']
            )
            self.__lines[line.get_name()] = line

        for trafo_data in substation['transformers']:
            transformer = Transformer(
                trafo_data['name'],
                trafo_data['voltage'],
                trafo_data['power'],
                trafo_data['hv'],
                trafo_data['lv'],
                trafo_data['connected_with'],
                trafo_data['switched_by']
            )
            self.__transformers[transformer.get_name()] = transformer

        for cb_data in substation['circuit_breakers']:
            cb = CircuitBreaker(cb_data['name'], cb_data['voltage'], cb_data['normal_state'])
            self.__circuit_breakers[cb.get_name()] = cb

        self.__load_protections(config['protection'])

    def __load_protections(self, protection_config: dict):
        for prot_type, prot_list in protection_config.items():
            self.__protections[prot_type] = []
            for p_data in prot_list:
                main_prot = MainProtection(
                    p_data['name_protected_equipment'],
                    p_data['setting'],
                    p_data['vendor'],
                    p_data['base'],
                    p_data['main_protection_failure_probability']
                )
                backup_prot = BackupProtection(
                    p_data['name_protected_equipment'],
                    p_data['setting'],
                    p_data['vendor'],
                    p_data['base'],
                    p_data['backup_protection_failure_probability']
                )
                self.__protections[prot_type].append({
                    'main': main_prot,
                    'backup': backup_prot
                })

    def get_all_equipment(self):
        equipment = {}
        equipment.update(self.__buses) #объединение всех словарей
        equipment.update(self.__lines)
        equipment.update(self.__transformers)
        return equipment

    def get_circuit_breakers(self) -> dict:
        return self.__circuit_breakers

    def get_buses(self) -> dict:
        return self.__buses

    def get_protections_for_equipment(self, equipment_name: str):
        for prot_type, prot_list in self.__protections.items(): #.items() = .__protections -> dict_items{[('line_protection_110', [{'main': <classes.protection.protection.Main...}],...)}
            for p in prot_list: #prot_type - 'line_protection_110'; prot_list - [{main1: <object1>, 'backup1': <object1b>}, {main2:...},]
                if p['main'].get_protected_equipment() == equipment_name:
                    return p
        return None

    def get_equipment_by_name(self, name: str):
        all_eq = self.get_all_equipment()
        return all_eq.get(name)

    def get_name(self) -> str:
        return self.__name

    def reset_all_protections(self):
        for prot_type, prot_list in self.__protections.items():
            for p in prot_list:
                p['main'].reset()
                p['backup'].reset()

    def reset_all_breakers(self):
        for cb in self.__circuit_breakers.values():
            cb.reset_to_normal()

    def get_all_protections(self):
        return self.__protections