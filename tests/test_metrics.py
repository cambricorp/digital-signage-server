import os, sys, urllib2, json, logging
from testkit import fetch, post
from nose.tools import ok_, eq_, istest, raises

sys.path.append('../lib')

log = logging.getLogger()

valid_data = {
    'playlist'    : "some_playlist",
    'mac_address' : "00:de:ad:be:ef:42",
    'ip_address'  : "127.0.0.1",
    'cpu_freq'    : 700,
    'cpu_temp'    : 45.0,
    'cpu_usage'   : 50,
    'browser_ram' : 192,
    'uptime'      : 0
}


def test_valid_data_point():
    """Valid POST payload"""

    res = post('metrics', valid_data)
    log.debug(res)


def test_invalid_data_point():
    """Invalid data of various kinds"""

    invalid_overrides = {
        'playlist'    : "some playlist",
        'mac_address' : "la di da",
        'ip_address'  : "localhost",
        'cpu_freq'    : 1.0,
        'cpu_temp'    : 45,
        'cpu_usage'   : "50",
        'browser_ram' : None,
    }

    for override in invalid_overrides:
        data = valid_data
        data[override] = invalid_overrides[override]
        res = post('metrics', data)
        log.debug(data)


@raises(urllib2.HTTPError)
def test_invalid_data_point():
    """Invalid POST payload"""

    data = post('metrics', {
        'playlist'    : "some_playlist",
        'uptime'      :0
    })
    log.debug(data)

