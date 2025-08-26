# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__maintainer__ = "Самков Н.А. https://online.sbis.ru/person/d4ea3ef3-98f2-4057-9c88-eee341795833"
__doc__ = "Функции работы с БД"

from .db import DBSession, Tea, Statistics, TeaRating, TeaType, StatReason


def create_tea(user_id: int, name: str) -> Tea:
    """Create Tea"""
    with DBSession() as session:
        tea = Tea(user_id=user_id, name=name)
        session.add(tea)
        session.commit()
        session.refresh(tea)
        return tea


def read_tea(tea_id: int) -> Tea:
    """Read Tea"""
    with DBSession() as session:
        return session.query(Tea).filter(Tea.id == tea_id).first()


def update_tea(tea_id: int, fields_to_update: dict) -> Tea:
    """Update Tea"""
    system_attrs = ['id', 'user_id', 'data', 'deleted']
    with DBSession() as session:
        if tea := session.query(Tea).filter(Tea.id == tea_id).first():
            for field, value in fields_to_update.items():
                if field in system_attrs:
                    continue
                if hasattr(tea, field):
                    setattr(tea, field, value)
            session.commit()
            session.refresh(tea)
        return tea


def delete_tea(tea_id: int) -> bool:
    """Delete Tea"""
    with DBSession() as session:
        if tea := session.query(Tea).filter(Tea.id == tea_id).first():
            tea.deleted = True
            session.commit()
            session.refresh(tea)
            return tea
        return False


def read_user_tea(user_id: int) -> list[Tea]:
    """Выборка всего чая пользователя"""
    with DBSession() as session:
        return session.query(Tea).filter(Tea.user_id == user_id, Tea.deleted != True).all()


def save_stat(tea_id: int, reason: StatReason = StatReason.PICK) -> None:
    """Зафиксировать выбор чая в статистику"""
    with DBSession() as session:
        if not session.query(Tea).filter(Tea.id == tea_id).first():
            return
        stat = Statistics(tea_id=tea_id, reason=reason)
        session.add(stat)
        session.commit()


def decrease_bags(tea_id: int) -> None:
    """Уменьшение количества пакетиков в наличии"""
    with DBSession() as session:
        if (tea := session.query(Tea).filter(Tea.id == tea_id).first()) and (tea.bags or 0) > 0:
            tea.bags -= 1
            session.commit()
            session.refresh(tea)
