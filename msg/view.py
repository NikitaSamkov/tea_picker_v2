# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__maintainer__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__doc__ = "Стандартные представления сущностей"

from data.db import Tea
from .formatting import escape_format


def get_tea_view(tea: Tea):
    """Возвращает описание чая"""
    result = [('*{}*', tea.name)]
    if tea.rating:
        result.append(('⭐' * tea.rating.value, None))
    if tea.description:
        result.append(('_{}_', tea.description))
    if tea.tea_type:
        result.append(('Тип: {}', tea.tea_type.value))
    if tea.bags is not None:
        result.append(('Осталось пакетиков: {}', tea.bags))
    if tea.location:
        result.append(('Расположение: {}', tea.location))
    if tea.use_sugar:
        result.append(('Пить с сахаром? {}\!', tea.use_sugar))
    text, args = zip(*result)
    return escape_format('\n'.join(text), *filter(None, args))
