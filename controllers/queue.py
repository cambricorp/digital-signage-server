#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Rui Carmo <rui.carmo@co.sapo.pt>
Description: Device controller class and helper functions
License: MIT (see LICENSE for details)
"""

import os, sys, logging

log = logging.getLogger()

from models import BaseController, Queue

class QueueController(BaseController):

    def push(self, mac_address, action, data):
        """Queue an action for a specific device"""
        q = Queue.create(
            mac_address = mac_address,
            action      = action,
            data        = data
        )
        q.save()