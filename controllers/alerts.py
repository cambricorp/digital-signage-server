'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

import os, sys, logging
from json import loads
from models.device import Device
from models.asset import Asset
from config import settings

log = logging.getLogger()

from base import BaseController

class AlertsController(BaseController):
    def __init__(self):
        super(AlertsController, self).__init__()

    def list_alerts(self, mac_address):
        return self.kv.list_alerts(mac_address)
    
    def pop_alerts(self, mac_address):
        return self.kv.pop_alerts(mac_address)
    
    def push_alert(self, mac_address_list, uri):
        for mac_address in mac_address_list:
            self.kv.push_alert(mac_address, uri)

    def list_templates(self):
        return settings.admin.alert_templates