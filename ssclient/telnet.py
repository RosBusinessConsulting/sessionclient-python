#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Sergey Sobko'
__email__ = 'ssobko@rbc.ru'
__copyright__ = 'Copyright 2014, RosBusinessConsulting'

import telnetlib


def _format_command(self, command, *args):
    """Formats commands to pass to telnet"""

    return '{command} {arguments}\n'.format(command=command, arguments=' '.join(args))


def write(telnet, command, *args):
    """Send command using Telnet protocol"""

    telnet.write(_format_command(command, *args))


def parse_response(response):
    """Parse key-value response"""

    response_dict = dict()
    response_string = response.split('\n')
    for kv in response_string:
        pair = kv.split('=')
        try:
            response_dict[pair[0]] = pair[1]
        except IndexError:
            pass
    return response_dict


def initialize_telnet(host, port):
    """Initialize telnet library"""

    return telnetlib.Telnet(host, port)
