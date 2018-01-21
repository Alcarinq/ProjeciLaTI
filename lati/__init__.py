# -*- coding: utf-8 -*-

import datetime
import logging
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.settings import asbool
from sqlalchemy import engine_from_config
from lati.models import DBSession, Base
from security import (RootFactory, groupfinder)
from pyramid_beaker import (session_factory_from_settings, set_cache_regions_from_settings)
from pyramid.renderers import JSON
from webassets import Bundle
from webassets.script import CommandLineEnvironment
from pyramid_webassets import get_webassets_env

log = logging.getLogger(__name__)


def include_views(config):
    '''Package modules
    '''
    config.add_route('home', '/')
    config.add_route('weather', '/weather')
    config.add_route('rental', '/rental')
    config.add_route('login', '/login')
    config.add_route('logoff', '/logoff')
    config.add_route('remove_rental', '/remove_rental/{id}')
    config.add_route('add_rental', '/add_rental/{id}')

def include_css(config):
    '''CSS
    '''
    theme = '.almost-flat'

    css = Bundle(
        'css/uikit%s.css' % theme,
        'css/datepicker%s.css' % theme,
        'css/layout.css',
        filters='cssmin', output='css/min-css.%(version)s.css')
    config.add_webasset('css', css)


def include_js(config):
    libraries = Bundle(
        'js/jquery.min.js',
        'js/jquery-ui.min.js',
        'js/jquery.nano.js',
        'js/uikit.js',
        'js/datepicker.js',
        'js/lati.app.js',
        filters='jsmin', output='js/min-libs.%(version)s.js')
    config.add_webasset('jslibraries', libraries)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    set_cache_regions_from_settings(settings)
    authentication_policy = AuthTktAuthenticationPolicy('seekrit', callback=groupfinder)
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory=RootFactory, authentication_policy=authentication_policy, authorization_policy=authorization_policy)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config.set_session_factory(session_factory_from_settings(settings))
    config.add_mako_renderer('.html')

    json_renderer = JSON()
    def datetime_adapter(obj, request):
        return obj.isoformat()
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    config.add_renderer('json', json_renderer)

    # Add static routes (required for static_path in Mako)
    config.add_static_view(name=settings.get('webassets.base_url'), path='static')
    config.include(include_views)
    config.include(include_css)
    config.include(include_js)
    config.scan()
    return config.make_wsgi_app()