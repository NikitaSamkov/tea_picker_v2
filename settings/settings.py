# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Модуль конфигураций"

import os
from configparser import ConfigParser


SETTINGS_DIR = os.path.dirname(__file__)
SETTINGS_FILENAME = os.path.join(SETTINGS_DIR, 'settings.ini')
SETTINGS_TEMPLATE_FILENAME = os.path.join(SETTINGS_DIR, 'settings.template')
WHITELIST_FILENAME = os.path.join(SETTINGS_DIR, 'security', 'whitelist.txt')

SETTINGS_DESCRIPTIONS = {
    'BOT_TOKEN': 'Токен бота',
    'ADMIN_ID': 'Телеграм ID администратора'
}


def init_settings() -> None:
    """Инициализация натроек"""
    tmpl = ConfigParser()
    tmpl.read(SETTINGS_TEMPLATE_FILENAME, encoding='utf-8')
    for section in tmpl.sections():
        for setting in tmpl.options(section):
            input_text = f'Введите значение для настройки "{SETTINGS_DESCRIPTIONS.get(setting.upper(), setting)}": '
            tmpl.set(section, setting, input(input_text))
    with open(WHITELIST_FILENAME, 'a', encoding='utf-8') as f:
        f.write(f'\n{tmpl.get("SECURITY", "ADMIN_ID")}')
    with open(SETTINGS_FILENAME, 'w', encoding='utf-8') as f:
        tmpl.write(f)


def get_settings() -> ConfigParser:
    """Возвращает настройки"""
    if not os.path.exists(SETTINGS_FILENAME):
        init_settings()
    settings = ConfigParser()
    settings.read(SETTINGS_FILENAME, encoding='utf-8')
    return settings
