#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Sergey Sobko'
__email__ = 'ssobko@rbc.ru'
__copyright__ = 'Copyright 2014, RosBusinessConsulting'


class NoMemcachedException(Exception):
    """No installed memcached library present"""

    pass


class FakeMemcachedClient(object):
    """Fake memcached client class"""

    def __init__(self, *args, **kwargs):
        raise NoMemcachedException

try:
    from pylibmc import Client as MemcachedClient
except ImportError:
    try:
        from memcache import Client as MemcachedClient
    except ImportError:
        MemcachedClient = FakeMemcachedClient


def initialize_memcached(memcached_nodes, memcached_configuration=None, logger=None):
    """Initialize memcached"""

    memcached_client = None
    if memcached_nodes:
        try:
            if isinstance(memcached_nodes, basestring) or isinstance(memcached_nodes, tuple):
                memcached_nodes = [memcached_nodes]
            else:
                memcached_nodes = memcached_nodes
            if memcached_configuration:
                memcached_client = MemcachedClient(memcached_nodes, **memcached_configuration)
            else:
                memcached_client = MemcachedClient(memcached_nodes)
        except Exception as e:
            if logger:
                logger.error(e)
    return memcached_client
