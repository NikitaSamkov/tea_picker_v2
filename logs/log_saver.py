# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Модуль логирования"

import os
from datetime import datetime


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
LOG_EXT = 'log'

def log_msg(msg: str):
    """Сохраняет сообщение в логи"""
    cur_time = datetime.now()
    filename = cur_time.strftime('%d-%m-%Y') + f'.{LOG_EXT}'
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    if not os.path.exists(os.path.join(DATA_DIR, filename)):
        with open(os.path.join(DATA_DIR, filename), 'a', encoding='utf-8'):
            pass
    with open(os.path.join(DATA_DIR, filename), 'a', encoding='utf-8') as f:
        f.write(f'[{cur_time.strftime("%H:%M:%S")}] {msg}\n')
