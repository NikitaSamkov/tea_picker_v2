# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Класс для команд, для которых аргументы отправляются отдельным сообщением"

from telegram import Update
from telegram.ext import CallbackContext


class SeparatedArguments:
    """Класс для команд, для которых аргументы отправляются отдельным сообщением"""
    WAITING_COMMANDS = {}

    @classmethod
    def wait(cls, user_id: int, callback, **kwargs):
        """Ожидать аргументов"""
        cls.WAITING_COMMANDS[user_id] = (callback, kwargs)

    @classmethod
    def reset(cls, user_id: int):
        """Перестать ожидать аргументы"""
        cls.WAITING_COMMANDS.pop(user_id, None)

    @classmethod
    async def run_callback(cls, update: Update, context: CallbackContext):
        """Вызов callback-функции с полученными аргументами"""
        callback, kwargs = cls.WAITING_COMMANDS.get(update.message.from_user.id, (None, None))
        if not callback:
            return
        return await callback(update, context, **kwargs)
