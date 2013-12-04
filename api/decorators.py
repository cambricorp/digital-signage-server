import os, sys, re
from bottle import request, abort
from utils.netstats import valid_ip_address, valid_mac_address

def valid_identifier(s):
    return True if re.match('^\w+$', s) else False

def valid_integer(s):
    return True if re.match('^\d+$', s) else False

def valid_float(s):
    return True if re.match('^\d+\.\d+$', s) else False

def check_valid_beacon():
    """Checks if POST data is valid"""

    def decorator(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            patterns = {
                'playlist'    : valid_identifier
                'mac_address' : valid_mac_address,
                'ip_address'  : valid_ip_address,
                'cpu_freq'    : valid_integer,
                'cpu_temp'    : valid_float,
                'cpu_usage'   : valid_integer,
                'browser_ram' : valid_integer,
                'uptime'      : valid_integer
            }
            for field in request.forms:
                if not patterns[field](request.forms.get(field)):
                    abort(406, "Not acceptable")
                    return
            if set(request.forms) != set(patterns):
                abort(406, "Not acceptable")
                return
            return callback(*args, **kwargs)
        return wrapper
    return decorator