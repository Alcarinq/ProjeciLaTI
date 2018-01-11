# -*- coding: utf-8 -*-

import datetime
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

import logging

log = logging.getLogger(__name__)


def include_views(config):
    '''Package modules/portal/__init__
    '''
    config.add_route('home', '/')

def include_css(config):
    '''Definicja modulow CSS
    '''
    theme = '.almost-flat'

    css = Bundle(
        'css/uikit%s.css' % theme,
        'css/components/accordion%s.css' % theme,
        'css/components/autocomplete%s.css' % theme,
        'css/components/datepicker%s.css' % theme,
        'css/components/dotnav%s.css' % theme,
        'css/components/form-advanced%s.css' % theme,
        'css/components/form-file%s.css' % theme,
        'css/components/form-password%s.css' % theme,
        'css/components/form-select%s.css' % theme,
        'css/components/notify%s.css' % theme,
        'css/components/placeholder%s.css' % theme,
        'css/components/progress%s.css' % theme,
        'css/components/search%s.css' % theme,
        'css/components/slidenav%s.css' % theme,
        'css/components/slider%s.css' % theme,
        'css/components/sticky%s.css' % theme,
        'css/components/tooltip%s.css' % theme,
        'css/components/upload%s.css' % theme,
        'css/layout.css',
        filters='cssmin', output='css/min-css.%(version)s.css')
    config.add_webasset('css', css)


def include_js(config):
    libraries = Bundle(
        'js/jquery.min.js',
        'js/jquery-ui.min.js',
        'js/jquery.nano.js',
        'js/angular.js',
        'js/angular-filter.min.js',
        'js/angular-animate.js',
        'js/nprogress.js',
        'js/chosen.jquery.js',
        'js/difflib.js',
        'js/diffview.js',
        'js/crossfilter.js',
        'js/dagre-d3.min.js',
        'js/graphlib-dot.min.js',
        'js/clipboard.js',
        'js/angular-drag-and-drop-lists.js',
        'js/uikit.js',
        'js/components/grid.js',
        'js/components/accordion.js',
        'js/components/pagination.js',
        'js/components/autocomplete.js',
        'js/components/notify.js',
        'js/components/sortable.js',
        'js/components/sticky.js',
        'js/components/upload.js',
        'js/components/datepicker.js',
        'js/components/search.js',
        'js/components/tooltip.js',
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