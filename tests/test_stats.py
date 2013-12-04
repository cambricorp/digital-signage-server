import os, sys, urllib2, json
from nose.tools import ok_, eq_, istest

sys.path.append('../lib')

import utils 
from config import settings

base_url = 'http://localhost:%d/api/v1/' % settings.http.port

def fetch(method):
    return json.loads(urllib2.urlopen(base_url + method).read())

def post(method, data):
    return json.loads(urllib2.urlopen(base_url + method, data).read())

def test_stats():
    """Valid POST payload"""
    data = post('stats', {
        'playlist'    : "some_playlist"
        'mac_address' : "00:de:ad:be:ef:42",
        'ip_address'  : "127.0.0.1",
        'cpu_freq'    : 700,
        'cpu_temp'    : 45.0,
        'cpu_usage'   : 50,
        'browser_ram' : 192,
        'uptime'      :0
    })
    print data
