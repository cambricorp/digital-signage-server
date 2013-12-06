import json, urllib, urllib2, logging
from config import settings

base_url = 'http://localhost:%d/api/v1/' % settings.http.port

log = logging.getLogger()

def fetch(method):
    return json.loads(urllib2.urlopen(base_url + method).read())

def post(method, data):
	payload = urllib.urlencode(data)
	return json.loads(urllib2.urlopen(base_url + method, payload).read())

