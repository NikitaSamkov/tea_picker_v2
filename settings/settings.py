# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Модуль конфигураций"

import os
from functools import lru_cache
from configparser import ConfigParser


SETTINGS_DIR = os.path.dirname(__file__)
SETTINGS_FILENAME = os.path.join(SETTINGS_DIR, 'settings.ini')
SETTINGS_TEMPLATE_FILENAME = os.path.join(SETTINGS_DIR, 'settings.template')
WHITELIST_FILENAME = os.path.join(SETTINGS_DIR, 'security', 'whitelist.txt')

SETTINGS_CACHE = None

SETTINGS_DESCRIPTIONS = {
    'BOT_TOKEN': 'Токен бота',
    'ADMIN_ID': 'Телеграм ID администратора',
    'UNIPIM': 'Токен авторизации на unipim.ru (получение товаров по штрихкоду)',
    'EAN_ONLINE': 'Токен авторизации на ean-online.ru (получение товаров по штрихкоду)',
    'EAN_DB': 'Токен авторизации на ean-db.com (получение товаров по штрихкоду)'
}


def init_settings() -> None:
    """Инициализация натроек"""
    print('[ИНИЦИАЛИЗАЦИЯ НАСТРОЕК]')
    settings = ConfigParser()
    verify_settings(settings)
    with open(WHITELIST_FILENAME, 'a', encoding='utf-8') as f:
        f.write(f'\n{settings.get("SECURITY", "ADMIN_ID")}')
    with open(SETTINGS_FILENAME, 'w', encoding='utf-8') as f:
        settings.write(f)


def verify_settings(settings: ConfigParser) -> None:
    """Проверка настроек"""
    print('[ПРОВЕРКА НАСТРОЕК]')
    tmpl = ConfigParser()
    tmpl.read(SETTINGS_TEMPLATE_FILENAME, encoding='utf-8')
    settings_sections = settings.sections()
    for section in tmpl.sections():
        if section not in settings_sections:
            settings.add_section(section)
        settings_options = settings.options(section)
        for option in tmpl.options(section):
            if option not in settings_options:
                input_text = f'Введите значение для настройки "{SETTINGS_DESCRIPTIONS.get(option.upper(), option)}": '
                settings.set(section, option, input(input_text))
    with open(SETTINGS_FILENAME, 'w', encoding='utf-8') as f:
        settings.write(f)


@lru_cache
def get_settings() -> ConfigParser:
    """Возвращает настройки"""
    if not os.path.exists(SETTINGS_FILENAME):
        init_settings()
    settings = ConfigParser()
    settings.read(SETTINGS_FILENAME, encoding='utf-8')
    verify_settings(settings)
    return settings
