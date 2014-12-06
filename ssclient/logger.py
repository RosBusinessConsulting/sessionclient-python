#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Sergey Sobko'
__email__ = 'ssobko@rbc.ru'
__copyright__ = 'Copyright 2014, RosBusinessConsulting'

import logging


def initialize_logger(logger=None):
    """Initialize logger"""

    if logger:
        if isinstance(logger, basestring):
            return logging.getLogger(logger)
        return logger
    return logging.getLogger('rbc.session')
