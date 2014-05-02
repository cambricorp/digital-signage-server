#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Rui Carmo (https://github.com/rcarmo)
Description: Feed controller class and helper functions
License: MIT (see LICENSE for details)
"""

import os, sys, logging
from json import loads
from config import settings
from models.consts import *
from utils.urlkit import fetch

log = logging.getLogger()

from base import BaseController

class FeedController(BaseController):
    def __init__(self):
        super(FeedController, self).__init__()

    @property
    def twitter_feed(self):
        try:
            return loads(self.kv.data.get(TWITTER_PF + "query"))
        except:
            return None

    @twitter_feed.setter
    def twitter_feed(self, data):
        self.kv.data.set(TWITTER_PF + "query", data)

    def get_stage_feed(self, stage):
        pass

    def get_site_feed(self, stage):
        pass

    def get_live_feed(self, stage):
        pass

    def get_feed(self, feed_name):
        if not feed_name in settings.feeds:
            raise Exception('Invalid feed name')

        feed_uri = settings.feeds[feed_name]

        return fetch(feed_uri)

