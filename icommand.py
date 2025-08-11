# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Команды бота"

import os
import json
from telegram import Update
from telegram.ext import CallbackContext
from functools import wraps

from logs import log_msg
from settings import is_admin, is_in_whitelist, get_settings
from separated_arguments import SeparatedArguments


def command_common(func):
    """Общий декоратор для команд бота"""
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext):
        try:
            user_info = update.message.from_user
            log_msg(f'{user_info.full_name} (@{user_info.username}) - {update.message.text}')
            SeparatedArguments.reset(update.message.from_user.id)
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


async def message_handler(update: Update, context: CallbackContext) -> None:
    """Обработка сообщений без команды"""
    user_info = update.message.from_user
    log_msg(f'{user_info.full_name} (@{user_info.username}) - {update.message.text}')
    await SeparatedArguments.run_callback(update, context)


@command_common
async def echo_comm(update: Update, context: CallbackContext) -> None:
    """Тест-эхо"""
    await update.message.reply_text('Пришлите мне текст для того,чтобы я его повторил!')
    SeparatedArguments.wait(update.message.from_user.id, echo_callback, prefix='Ваше сообщение: ')


async def echo_callback(update: Update, context: CallbackContext, prefix = '') -> None:
    """callback-функция для echo"""
    await update.message.reply_text(f'{prefix} {update.message.text}')

