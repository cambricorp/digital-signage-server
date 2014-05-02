#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Hugo Lima (https://github.com/hmiguellima)
Description: Base controller logic
License: MIT (see LICENSE for details)
"""

from logging import log
from models.kv_store import KeyValueStore

class BaseController(object):
    """A base controller class that knows about the data stores"""

    def __init__(self):
        self.kv = KeyValueStore()
