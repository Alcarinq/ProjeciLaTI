# -*- coding: utf-8 -*-

import logging

from pyramid.view import (view_config, forbidden_view_config)
from pyramid.security import (Deny, Allow, Everyone, Authenticated)
from datetime import datetime
from lati.models import (Base, DBSession, Test)

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
        date = datetime.now().strftime('%d-%m-%Y')
        weekday = datetime.now().today().weekday()

        item = DBSession.query(Test).filter(Test.id == weekday).first()

        return dict(date=date, openHour=item.openHour, closeHour=item.closeHour, rOpenHour=item.rOpenHour, rCloseHour=item.rCloseHour)