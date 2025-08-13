# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__maintainer__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__doc__ = "Функции для работы с сущностью Чай"

from telegram import Update
from telegram.ext import CallbackContext
from data.db_service import create_tea


async def add_tea(update: Update, name) -> None:
    """Добавить чай"""
    if create_tea(update.message.from_user.id, name):
        await update.message.reply_text('Чай успешно добавлен!')
    else:
        await update.message.reply_text('Не удалось добавить чай! Попробуйте позднее.')
