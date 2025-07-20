# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Основной модуль для запуска бота"

from telegram.ext import Application, CommandHandler
from settings import get_settings
from icommand import start_comm, error_hndl


bot_settings = get_settings()


def main():
    application = Application.builder().token(bot_settings.get('BOT', 'BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start_comm))
    application.add_error_handler(error_hndl)

    print('БОТ ЗАПУЩЕН')
    application.run_polling()


if __name__ == '__main__':
    main()
