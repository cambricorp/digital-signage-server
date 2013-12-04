#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Worker tasks

Created by: Rui Carmo
"""

import os, sys, re, functools, logging
from bottle import request, abort
from utils.netstats import valid_ip_address, valid_mac_address

log = logging.getLogger()

def valid_identifier(s):
    return True if re.match('^\w+$', s) else False

def valid_integer(s):
    return True if re.match('^\d+$', s) else False

def valid_float(s):
    return True if re.match('^\d+\.\d+$', s) else False


def check_valid_beacon(callback):
    """Checks if POST data is valid - has to be inserted _after_ the @post decorator"""
    
    @functools.wraps(callback)
    def wrapper(*args, **kwargs):
        patterns = {
            'playlist'    : valid_identifier,
            'mac_address' : valid_mac_address,
            'ip_address'  : valid_ip_address,
            'cpu_freq'    : valid_integer,
            'cpu_temp'    : valid_float,
            'cpu_usage'   : valid_integer,
            'browser_ram' : valid_integer,
            'free_ram'    : valid_integer,
            'free_disk'   : valid_integer,
            'uptime'      : valid_integer,
            'tx_bytes'    : valid_integer,
            'rx_bytes'    : valid_integer,
        }
        for required in ['mac_address','ip_address']:
            if required not in request.forms:
                abort(406, "Not acceptable")
                return                
        for field in request.forms:
            res = patterns[field](request.forms.get(field))
            log.debug("%s:%s" % (field, res))
            if not res:
                abort(406, "Not acceptable")
                return
        if set(request.forms) != set(patterns):
            abort(406, "Not acceptable")
            return
        return callback(*args, **kwargs)
    return wrapper
