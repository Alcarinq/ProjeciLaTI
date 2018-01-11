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
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    testColumn = Column(DateTime(timezone=False), nullable=False, default='')

    def __json__(self, request):
        return {
            'code': self.code,
            'description': self.description,
            'is_admin': self.is_admin,
            'membership' : self.membership
        }
