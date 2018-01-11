# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(expire_on_commit=False, extension=ZopeTransactionExtension()))

Base = declarative_base()

from dblen import *

# Add others models here
from db.public import *
