# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__maintainer__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__doc__ = "Форматирование ответов от бота"

import re


def escape_markdown(text: str) -> str:
    """Экранирование текста для markdown"""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)


def escape_format(text: str, *args):
    """Экранирование текста с форматированием для markdown"""
    return text.format(*map(escape_markdown, args))
