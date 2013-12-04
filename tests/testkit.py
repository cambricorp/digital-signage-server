import json, urllib, urllib2
from config import settings

base_url = 'http://localhost:%d/api/v1/' % settings.http.port

def fetch(method):
    return json.loads(urllib2.urlopen(base_url + method).read())

def post(method, data):
    return json.loads(urllib2.urlopen(base_url + method, urllib.urlencode(data)).read())

