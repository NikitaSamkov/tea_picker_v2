# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Модуль безопасности"

import os
from ..settings import get_settings


ADMIN_ID = get_settings().get('SECURITY', 'ADMIN_ID')
WHITELIST_PATH = os.path.join(os.path.dirname(__file__), 'whitelist.txt')


def is_admin(user_id: int) -> bool:
    """Проверяет, совпадает ли идентификатор пользователя с идентификатором администратора

    Args:
        user_id (int): Идентификатор пользователя

    Returns:
        bool: Результат
    """
    return str(user_id) == ADMIN_ID


def is_in_whitelist(user_id: int) -> bool:
    """Проверяет, есть ли идентификатор пользователя в белом списке

    Args:
        user_id (int): Идентификатор пользователя

    Returns:
        bool: Результат
    """
    with open(WHITELIST_PATH, 'r', encoding='utf-8') as f:
        return str(user_id) in f.readlines()
