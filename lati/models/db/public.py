# -*- coding: utf-8 -*-

from sqlalchemy import (
    ForeignKey,
    Column,
    Boolean,
    Integer,
    UnicodeText,
    Unicode,
    String,
    Table,
    DateTime,
    text,
    LargeBinary
    )

import json

from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy.orm import relationship, deferred
from sqlalchemy.schema import (UniqueConstraint)
from sqlalchemy import desc, asc

from lati.models import Base

from ..dblen import DBLimits

class Test(Base):
    __tablename__ = 'Test'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    openHour = Column(UnicodeText(), nullable=True)
    closeHour = Column(UnicodeText(), nullable=True)
    rOpenHour = Column(UnicodeText(), nullable=True)
    rCloseHour = Column(UnicodeText(), nullable=True)

    def __json__(self, request):
        return {
            'openHour': self.openHour,
            'closeHour': self.closeHour,
            'rOpenHour': self.rOpenHour,
            'rCloseHour': self.rCloseHour
        }

class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    login = Column(UnicodeText(), nullable=False)
    password = Column(UnicodeText(), nullable=False)
    group = Column(UnicodeText(), nullable=False)

    def __json__(self, request):
        return {
            'login': self.login,
            'password': self.password,
            'group': self.group
        }

class Stuff(Base):
    __tablename__ = 'Stuff'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    name = Column(UnicodeText(), nullable=False)
    price = Column(Integer, nullable=False)
    rent = Column(Boolean, nullable=False)
    rent_by = Column(UnicodeText(), nullable=True)
    rent_date = Column(DateTime, nullable=True)

    def __json__(self, request):
        return {
            'name': self.name,
            'price': self.price,
            'rent': self.rent,
            'rent_by': self.rent_by,
            'rent_date': self.rent_date
        }