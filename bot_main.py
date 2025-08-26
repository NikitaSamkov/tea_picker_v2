# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Основной модуль для запуска бота"

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from settings import get_settings
from icommand import start_comm, echo_comm, add_tea_comm, tea_list_comm, pick_comm, delete_comm
from icommand import delete_button
from icommand import error_hndl, message_handler
from icommand import ACTIVE_CALLBACKS


bot_settings = get_settings()


def main():
    application = Application.builder().token(bot_settings.get('BOT', 'BOT_TOKEN')).build()

    add_command(application, 'start', start_comm)
    add_command(application, 'echo', echo_comm)
    add_command(application, 'add_tea', add_tea_comm)
    add_command(application, 'tea_list', tea_list_comm)
    add_command(application, 'pick', pick_comm)
    add_command(application, 'delete', delete_comm)

    application.add_error_handler(error_hndl)
    application.add_handler(MessageHandler(filters.ALL, callback=message_handler))
    application.add_handler(CallbackQueryHandler(get_button_handler([
        (lambda u, _: u.callback_query.data.startswith('del:'), delete_button)
    ])))

    print('БОТ ЗАПУЩЕН')
    application.run_polling()


def add_command(application: Application, command: str, callback):
    """Добавить команду и записать её в /start"""
    application.add_handler(CommandHandler(command, callback))
    ACTIVE_CALLBACKS[command] = callback


def get_button_handler(bindings: list[tuple]):
    async def button_handler(update, context):
        await update.callback_query.answer()
        for condition, callback in bindings:
            if condition(update, context):
                await callback(update, context)
                return
    return button_handler


if __name__ == '__main__':
    main()
