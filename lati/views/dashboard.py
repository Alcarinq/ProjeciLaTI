# -*- coding: utf-8 -*-

import logging

from itertools import groupby

from pyramid.view import (view_config, forbidden_view_config)
from pyramid.security import (Deny, Allow, Everyone, Authenticated)

import webhelpers.paginate as paginate

log = logging.getLogger(__name__)

class DashboardView(object):
    __acl__ = []

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = request.session
        self.settings = request.registry.settings


    @view_config(route_name='home', renderer='lati:templates/main.html')
    def home(self):
        return dict()