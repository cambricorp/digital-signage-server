'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

import os, sys, logging
from json import loads
from models.device import Device
from models.asset import Asset

log = logging.getLogger()

from base import BaseController

class AssetController(BaseController):
    def __init__(self):
        super(AssetController, self).__init__()

    def get_asset(self, guid):
        return self.kv.get_asset(guid)

    def get_all_assets(self):
        return self.kv.list_assets()

    def set_asset(self, guid, description, type, uri, duration_secs=None, pin=None, how_many=None, shuffle=None):
        self.kv.set_asset(guid, Asset(uri, guid, description, type, duration_secs, pin, how_many, shuffle))

    def delete_asset(self, guid):
        self.kv.delete_asset(guid)
