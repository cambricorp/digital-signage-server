#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Rui Carmo <rui.carmo@co.sapo.pt>
Description: Device controller class and helper functions
License: MIT (see LICENSE for details)
"""

import os, sys, logging

log = logging.getLogger()

from models import BaseController

class DeviceController(BaseController):

    def get_all_devices(self):
        """Shorthand for returning data on all devices as a dictionary"""
        d = Device.select().order_by(Device.last_seen.desc())
        return [x._data for x in d]