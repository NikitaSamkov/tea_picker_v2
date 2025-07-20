# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Команды бота"

from telegram import Update
from telegram.ext import CallbackContext
from functools import wraps

from logs import log_msg
from settings import is_admin, is_in_whitelist


def command_common(func):
    """Общий декоратор для команд бота"""
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext):
        try:
            user_info = update.message.from_user
            log_msg(f'{user_info.full_name} (@{user_info.username}) - {update.message.text}')
        except Exception as e:
            print(f'Произошла ошибка: {e}')
        return await func(update, context)
    return wrapper


def admin_only(func):
    """Декоратор проверки на администратора"""
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext):
        if not is_admin(update.message.from_user.id):
            return await update.message.reply_text('У вас недостаточно прав для вызова этой команды!')
        return await func(update, context)
    return wrapper


def whitelist_only(func):
    """Декоратор проверки на нахождение пользователя в белом списке"""
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext):
        if not is_in_whitelist(update.message.from_user.id):
            return await update.message.reply_text('У вас недостаточно прав для вызова этой команды!')
        return await func(update, context)
    return wrapper


@command_common
async def start_comm(update: Update, context: CallbackContext) -> None:
    """Команда start"""
    await update.message.reply_text("""
Привет! Я умею работать со следующими командами:
/start - Показывает текущее сообщение
""")


@command_common
def error_hndl(update: Update, context: CallbackContext) -> None:
    """Обработка ошибок"""
    log_msg(f'Произошла ошибка: {context.error}')
    print(f'Update {update} caused error {context.error}')
