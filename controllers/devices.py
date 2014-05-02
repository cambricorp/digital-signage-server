#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Hugo Lima (https://github.com/hmiguellima)
Description: Device controller class and helper functions
License: MIT (see LICENSE for details)
"""

import os, sys, logging
from json import loads
from models.device import Device

log = logging.getLogger()

from base import BaseController

class DeviceController(BaseController):
    def __init__(self):
        super(DeviceController, self).__init__()

    def get_all_devices(self):
        return self.kv.list_devices()

    def set_device(self, mac_address, ip_address, name, active, version, playlist):
        self.kv.set_device(mac_address, Device(mac_address, ip_address, name, active, version, playlist))

    def get_device(self, mac_address):
        return self.kv.get_device(mac_address)

    def delete_device(self, mac_address):
        self.kv.delete_device(mac_address)
