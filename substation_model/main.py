"""
Программа моделирования нарушений
"""

import random
from time import sleep
from classes.system.substation import Substation
from classes.system.logger import setup_logger
from classes.faults.fault import FaultFactory
from utils.random_generator import select_random_equipment


def main():
    logger = setup_logger()
    logger.info("=" * 80)
    logger.info("ЗАПУСК МОДЕЛИ ПОДСТАНЦИИ 110/10 кВ)")
    logger.info("=" * 80)

    substation = Substation('config/substation_config.json')
    logger.info(f"Подстанция загружена: {substation.get_name()}")

    iteration = 0
    max_iterations = 10

    while iteration < max_iterations:
        sleep(1)
        iteration += 1
        logger.info(f"{'=' * 15} ИТЕРАЦИЯ {iteration}/{max_iterations} {'=' * 15}")

        substation.reset_all_protections()
        substation.reset_all_breakers()

        equipment = substation.get_all_equipment()
        #equipment = substation.get_buses()
        eq_name, eq_object = select_random_equipment(equipment)

        voltage = eq_object.get_voltage()
        fault_type = FaultFactory.get_random_fault_type(eq_object.get_type())
        fault = FaultFactory.create_fault(fault_type, voltage)
        fault_current = fault.calculate_fault_current()

        logger.info(f"Повреждённый элемент: {eq_name} ({eq_object.get_type()})")
        logger.info(f"Тип КЗ: {fault.get_fault_type()}")
        logger.info(f"Ток КЗ: {fault_current:.2f} А")

        protection = substation.get_protections_for_equipment(eq_name)

        main_prot = protection['main']
        backup_prot = protection['backup']

        protection_operated = False
        protection_type = ""
        disconnected_breakers = []

        if main_prot.check_fault(fault_current):
            protection_operated = True
            protection_type = "Основная"
            logger.info(f"Сработала защита: {protection_type} ({main_prot.get_setting():.1f} А)")
        elif backup_prot.check_fault(fault_current):
            logger.info(f"Основная защита не сработала")
            sleep(0.5)
            protection_operated = True
            protection_type = "Резервная"
            logger.info(f"Сработала защита: {protection_type} ({backup_prot.get_setting():.1f} А)")

        if protection_operated:
            switched_by = eq_object.get_switched_by()
            circuit_breakers = substation.get_circuit_breakers()

            for cb_name in switched_by:
                if cb_name in circuit_breakers and (circuit_breakers[cb_name].get_state() != 'open'):
                    circuit_breakers[cb_name].switch_off()
                    disconnected_breakers.append(cb_name)

            logger.info(f"Результат работы защиты: Успешно ({protection_type})")
            logger.info(f"Отключенные выключатели: {', '.join(disconnected_breakers) if disconnected_breakers else 'нет'}")
        else:
            logger.error("Результат работы защиты: ОТКАЗ (обе защиты не сработали)")
            logger.info("Отключенные выключатели: нет")

    logger.info(f"{'=' * 80}")
    logger.info("МОДЕЛИРОВАНИЕ ЗАВЕРШЕНО")
    logger.info(f"{'=' * 80}")

    #print(substation.get_all_protections().items())



if __name__ == "__main__":
    main()