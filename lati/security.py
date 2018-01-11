# -*- coding: utf-8 -*-

from socket import getaddrinfo

from pyramid.security import (Allow, Authenticated, DENY_ALL, ALL_PERMISSIONS)

import logging

log = logging.getLogger(__name__)
seclog = logging.getLogger('security')


class RootFactory(object):
    __acl__ = [
        (Allow, 'admins', ALL_PERMISSIONS),
        DENY_ALL,
    ]


    def __init__(self, request):
        pass

def groupfinder(userid, request):
    """Find groups for a given user
    """
    return request.session.get('roles', [])
