# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Основной модуль для запуска бота"

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from settings import get_settings
from icommand import start_comm, echo_comm
from icommand import error_hndl, message_handler


bot_settings = get_settings()


def main():
    application = Application.builder().token(bot_settings.get('BOT', 'BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start_comm))
    application.add_handler(CommandHandler("echo", echo_comm))
    application.add_error_handler(error_hndl)
    application.add_handler(MessageHandler(filters.ALL, callback=message_handler))

    print('БОТ ЗАПУЩЕН')
    application.run_polling()


if __name__ == '__main__':
    main()
