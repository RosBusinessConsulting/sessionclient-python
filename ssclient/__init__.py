#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Sergey Sobko'
__email__ = 'ssobko@rbc.ru'
__copyright__ = 'Copyright 2014, RosBusinessConsulting'

from .memcached import initialize_memcached
from .logger import initialize_logger
from .telnet import initialize_telnet, write, parse_response

SESSIONCLIENT_VERSION = 'python/script'
MEMCACHED_PREFIX = 'session_'


class Session(object):
    def __init__(self, host='localhost', port='8080',
                 memcached_nodes=None, memcached_configuration=None,
                 logger_configuration=None):
        """Initialize object"""

        self.host = host
        self.port = port

        self.logger = initialize_logger(logger_configuration)
        self.memcached = initialize_memcached(memcached_nodes, memcached_configuration, self.logger)

    def create(self, user, password):
        """Create session"""

        tn = initialize_telnet(self.host, self.port)

        write(tn, 'VERSION', SESSIONCLIENT_VERSION)
        write(tn, 'CREATE_SESSION', user, password)
        response = parse_response(tn.read_all())

        self.memcached.set(MEMCACHED_PREFIX + response['session_id'], response)

        return response

    def check(self, session):
        """Check session"""

        response = None
        if self.memcached:
            response = self.memcached.get(MEMCACHED_PREFIX + session)

        if not response:
            tn = initialize_telnet(self.host, self.port)

            write(tn, 'VERSION', SESSIONCLIENT_VERSION)
            write(tn, 'CHECK_SESSION', session)
            response = parse_response(tn.read_all())

        return response

    def delete(self, session):
        """Delete session"""

        tn = initialize_telnet(self.host, self.port)

        write(tn, 'VERSION', SESSIONCLIENT_VERSION)
        write(tn, 'DELETE_SESSION', session)
        response = parse_response(tn.read_all())

        if self.memcached:
            self.memcached.delete(MEMCACHED_PREFIX + session)

        return response
