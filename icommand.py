# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Команды бота"

import os
import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from functools import wraps

from logs import log_msg
from settings import is_admin, is_in_whitelist, get_settings
from separated_arguments import SeparatedArguments

from data.db import StatReason
from data.db_service import read_user_tea, save_stat, decrease_bags, delete_tea
from msg.view import get_tea_view
from tea.utils import add_tea


ACTIVE_CALLBACKS = {}


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
    """Вывести информацию о всех доступных командах"""
    preamble = 'Привет! Я умею работать со следующими командами:'
    commands_info = '\n'.join(f'/{comm} - {callback.__doc__}' for comm, callback in ACTIVE_CALLBACKS.items())
    await update.message.reply_text(f'{preamble}\n{commands_info}')


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
    """Повторить написанное сообщение"""
    await update.message.reply_text('Пришлите мне текст для того,чтобы я его повторил!')
    SeparatedArguments.wait(update.message.from_user.id, echo_callback, prefix='Ваше сообщение: ')


async def echo_callback(update: Update, context: CallbackContext, prefix = '') -> None:
    """callback-функция для echo"""
    await update.message.reply_text(f'{prefix} {update.message.text}')


@command_common
async def add_tea_comm(update: Update, context: CallbackContext) -> None:
    """Добавить чай в пул"""
    if context.args:
        return await add_tea(update, ' '.join(context.args))

    await update.message.reply_text('Напишите мне название чая.')
    SeparatedArguments.wait(update.message.from_user.id, add_tea_callback)


async def add_tea_callback(update: Update, context: CallbackContext) -> None:
    """callback-функция для add_tea"""
    await add_tea(update, update.message.text)


@command_common
async def tea_list_comm(update: Update, context: CallbackContext) -> None:
    """Список чая"""
    if user_tea := read_user_tea(update.message.from_user.id):
        await update.message.reply_text('Ваш список чая:\n\n' + '\n'.join(map(lambda item: item.name, user_tea)))
    else:
        await update.message.reply_text('У вас нет ни одного чая.\nДобавить чай можно командой /add_tea')


@command_common
async def pick_comm(update: Update, context: CallbackContext) -> None:
    """Выбрать случайный чай из пула"""
    user_tea = read_user_tea(update.message.from_user.id)
    if not user_tea:
        return await update.message.reply_text('У вас нет ни одного чая.\nДобавить чай можно командой /add_tea')

    result = random.choice(user_tea)
    save_stat(result.id, StatReason.PICK)
    decrease_bags(result.id)
    await update.message.reply_text(get_tea_view(result), parse_mode='MarkdownV2')


@command_common
async def delete_comm(update: Update, context: CallbackContext) -> None:
    """Удалить чай из пула"""
    user_tea = read_user_tea(update.message.from_user.id)
    if not user_tea:
        return await update.message.reply_text('У вас нет ни одного чая.\nДобавить чай можно командой /add_tea')
    if len(user_tea) > 4:
        keyboard = [
            list(map(lambda tea: InlineKeyboardButton(tea.name, callback_data=f'del:{tea.id}'), user_tea[i:i+2]))
            for i in range(0, len(user_tea), 2)
        ]
    else:
        keyboard = [[InlineKeyboardButton(tea.name, callback_data=f'del:{tea.id}')] for tea in user_tea]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите чай, который хотите удалить из пула:', reply_markup=reply_markup)


async def delete_button(update: Update, context: CallbackContext) -> None:
    """Обработчик кнопки удаления"""
    query = update.callback_query
    tea_id = int(query.data.split(':')[1])
    status = delete_tea(tea_id)
    if status:
        await query.edit_message_text(text=f"Успешно удалён чай {status.name} из пула!")
    else:
        await query.edit_message_text(text=f"Не удалось удалить чай из пула")
