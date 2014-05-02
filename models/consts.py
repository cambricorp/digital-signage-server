#!/bin/env python
"""
Created on Mar 26, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
"""

from config import settings

""" Redis key prefixes """
DEVICE_PF   = settings.redis.base+'device#'
ASSET_PF    = settings.redis.base+'asset#'
PLAYLIST_PF = settings.redis.base+'playlist#'
STATS_PF    = settings.redis.base+'stats#'
ALERTS_PF   = settings.redis.base+'alerts#'
TWITTER_PF  = settings.redis.base+'twitter#'
ASSETLIST_PF  = settings.redis.base+'assetlist#'
MEOKANAL_PF =  settings.redis.base+'meolist#'

MAX_STAT_ITEMS  = 100  # Maximum number of kept log items for a single device
MAX_ALERT_ITEMS = 5    # Maximum number of kept alerts for a single device
