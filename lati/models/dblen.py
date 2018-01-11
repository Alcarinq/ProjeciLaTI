# -*- coding: utf-8 -*-

class DBLimits(object):
    '''DB fields length
    '''
    max_items = 300
    dashboard_items = 10

    CODE = 50         # General purpose cade field
    NAME = 250        # General purpose name field
    DESC = 512        # General purpose description field
    CAT = 80          # Category field
    ENUM = 2          # Generic purpose enum field
    PROBLEMKEY = 100  # Problem key
    VERSION = 30      # General purpose version field
    SVNPATH = 512     # SVN path
    PATH = 512        # File path
