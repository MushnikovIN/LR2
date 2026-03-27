"""
Модуль настройки логгера для моделирования работы подстанции.

Этот модуль отвечает за создание и настройку объекта логгера, который используется
для записи событий в процессе симуляции. Логгер позволяет:
- Записывать подробные отладочные данные в файл (уровень DEBUG)
- Выводить важную информацию в консоль (уровень INFO)
- Структурировать сообщения с временными метками и уровнями важности
"""

import logging
import os


def setup_logger(log_file: str = 'logs/events.log') -> logging.Logger:
    """
    Создаёт и настраивает логгер для записи событий симуляции.
    
    :param log_file: Путь к файлу для записи логов (по умолчанию 'logs/events.log')
    :return: Настроенный объект логгера
    """
    # Создаём директорию для логов, если она не существует
    # exist_ok=True предотвращает ошибку, если папка уже существует
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Создаём именованный логгер для проекта substation_model
    logger = logging.getLogger('substation_model')
    logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень для обработки сообщений

    # Обработчик для записи логов в файл (сохраняет все сообщения включая DEBUG)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Обработчик для вывода логов в консоль (только важные сообщения INFO и выше)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Форматтер определяет структуру записи лога:
    # дата/время | уровень | сообщение
    formatter = logging.Formatter(
        '%(asctime)s:%(msecs)03d | %(levelname)-4s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Применяем формат к обоим обработчикам
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger