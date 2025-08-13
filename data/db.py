# -*- coding: utf-8 -*-
__author__ = "Самков Н.А. https://github.com/NikitaSamkov"
__maintainer__ = "Самков Н.А. https://github.com/NikitaSamkov"
__doc__ = "Модели БД"

import enum
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Enum, Text, JSON, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableDict


DATABASE_URL = 'sqlite:///data/tea_bot.db'
engine = create_engine(DATABASE_URL, echo=True)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class TeaRating(enum.Enum):
    STAR_1 = 1
    STAR_2 = 2
    STAR_3 = 3
    STAR_4 = 4
    STAR_5 = 5


class TeaType(enum.Enum):
    GREEN = 'Зеленый'
    BLACK = 'Черный'
    WHITE = 'Белый'
    RED = 'Красный'
    HERBAL = 'Травяной'
    OTHER = 'Другое'


class StatReason(enum.Enum):
    PICK = 'pick'
    FILL_CUP = 'fill_cup'


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc)
    )


class Tea(Base):
    __tablename__ = 'tea'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255))
    bags = Column(Integer)
    rating = Column(Enum(TeaRating))
    description = Column(Text())
    use_sugar = Column(Boolean)
    picked = Column(Integer, default=0)
    tea_type = Column(Enum(TeaType))
    location = Column(Text)
    data = Column(MutableDict.as_mutable(JSON))
    deleted = Column(Boolean, default=False)

    statistics = relationship('Statistics', back_populates="tea", cascade="all, delete-orphan")


class Statistics(Base, CreatedAtMixin):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tea_id = Column(Integer, ForeignKey("tea.id"), nullable=False)
    reason = Column(Enum(StatReason), default=StatReason.PICK)

    tea = relationship('Tea', back_populates="statistics")