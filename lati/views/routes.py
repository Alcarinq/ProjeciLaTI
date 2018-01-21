# -*- coding: utf-8 -*-

import logging
import random

from pyramid.view import (view_config, forbidden_view_config)
from pyramid.security import (Deny, Allow, Everyone, Authenticated)
from datetime import datetime
from lati.models import (Base, DBSession, Test, Users, Stuff)
from random import randint
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import has_permission

import sys

log = logging.getLogger(__name__)

class DashboardView(object):
    __acl__ = []

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.session = request.session
        self.settings = request.registry.settings
        reload(sys)
        sys.setdefaultencoding('utf-8')

    @view_config(route_name='home', renderer='lati:templates/main.html')
    def home(self):
        date = datetime.now().strftime('%d-%m-%Y')
        weekday = datetime.now().today().weekday()

        item = DBSession.query(Test).filter(Test.id == weekday).first()

        return dict(date=date, openHour=item.openHour, closeHour=item.closeHour, rOpenHour=item.rOpenHour, rCloseHour=item.rCloseHour)

    @view_config(route_name='weather', renderer='lati:templates/weather.html')
    def weather(self):
        return dict()

    @view_config(route_name='rental', renderer='lati:templates/rental.html')
    def rental(self):
        data = DBSession.query(Stuff).all()
        return dict(data=data)

    @view_config(route_name='remove_rental', renderer='json')
    def remove_rental(self):
        id_ = self.request.matchdict.get('id')
        data = DBSession.query(Stuff).filter(Stuff.id == id_).first()
        if data:
            if data.rent:
                data.rent = False
                data.rent_by = None
                data.rent_date = None
        return dict()

    @view_config(route_name='add_rental', renderer='json')
    def add_rental(self):
        request = self.request
        rent_by = request.params['rent_by']
        rent_date = request.params['rent_date']

        id_ = self.request.matchdict.get('id')
        #rent_by = "TEST"
        #rent_date = datetime.now().strftime('%Y-%m-%d')
        data = DBSession.query(Stuff).filter(Stuff.id == id_).first()
        if data:
            data.rent = True
            data.rent_by = rent_by
            data.rent_date = rent_date
        return dict()

    @view_config(context=HTTPForbidden, renderer='lati:templates/login.html')
    @view_config(route_name='login', renderer='lati:templates/login.html')
    def login(self):
        request = self.request
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            user = DBSession.query(Users).filter(Users.login == login).filter(Users.password == password).first()
            if user:
                session = request.session
                session['logged'] = 'yes'
                session['group'] = user.group
                headers = remember(request, login)
                return HTTPFound(location=request.route_url('home'), headers=headers)
        return dict(
            url=request.route_url('login'),
            login=login,
            password=password,
            )

    @view_config(route_name='logoff', renderer='json')
    def logout(self):
        request = self.request
        headers = forget(request)
        session = request.session
        session.clear()
        session.save()
        url = request.route_url('home')
        return HTTPFound(location=url, headers=headers)