'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

import os, sys, logging
from json import loads
from models.device import Device
from models.asset import Asset
from models.playlist import Playlist
from models.stats import Stats

log = logging.getLogger()

from base import BaseController

class StatsController(BaseController):
    def __init__(self):
        super(StatsController, self).__init__()

    def list_stats(self, mac_address):
        return self.kv.list_stats(mac_address)

    def push_stats(self, mac_address, date_time, state, debug_message):
        self.kv.push_stats(mac_address, Stats(date_time, state, debug_message))
