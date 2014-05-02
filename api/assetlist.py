#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Administration backend API

Created by: Hugo Lima (https://github.com/hmiguellima)
Contributors: Bruno Santos (https://github.com/brunorene)
"""

import os, sys, logging, time, copy
from json import dumps, loads
from bottle import route, get, put, post, delete, request, response, abort, redirect
import api
from controllers.assetlist import AssetlistController
import uuid
from redis import StrictRedis as Redis
from config import settings
from controllers.devices import DeviceController
from controllers.playlists import PlaylistController
from tasks.assetlist import refresh_assetlists
from controllers.alerts import AlertsController
import hashlib

log = logging.getLogger()

from decorators import timed, jsonp, cache_results, redis_cache

alc = AssetlistController()
dc  = DeviceController()
ac  = AlertsController()

prefix = api.prefix + '/assetlist'
meokanal_prefix = api.prefix + '/meokanal'

# Playlists

@get(prefix + '/<mac_addr>/<ip>')
@timed
@jsonp
def get_assetlist(mac_addr, ip):
    """Returns the current asset list for a given device"""
    
    # TODO: validate arguments

    # if we have a pending alert for this device, then return them right away as a one-off "playlist"
    alerts = ac.pop_alerts(mac_addr)
    if alerts is not None and len(alerts) > 0:
        alert_list = {"guid": uuid.uuid4().hex, "assets": []}
        for alert in alerts:
            duration, url = alert.split(",", 1)
            alert_list["assets"].append({'guid': hashlib.sha256(url).hexdigest(), 'type': 'alert', 'duration_secs': int(duration), 'uri': url})
        log.debug(alert_list)
        return {"info": alert_list, "alerts": True}

    device = dc.get_device(mac_addr) 
    if device is None:
        dc.set_device(mac_addr, ip, "plasma {}".format(mac_addr), True , 1, "DefaultList")
        refresh_assetlists()

    device = dc.get_device(mac_addr)
    dc.set_device(mac_addr, ip, device["name"], device["active"], device["version"], device["playlist"])
    result = alc.get_assetlist(mac_addr)

    if not result:
        return None

    for asset in result.info.assets:
        if asset["uri"][0] == "/":
            asset["uri"] = "{}://{}/signage{}".format(request.urlparts.scheme, request.urlparts.netloc, asset["uri"]) 
    result["alerts"] = False
    return result

r = Redis(**settings.redis.server)

@get(meokanal_prefix + '/<aid>/<idx>')
@timed
def resolve_meokanal_item(aid, idx):
    """Resolves a MEO Kanal item to a load balancer URI, ensuring freshness."""

    link = alc.resolve_meo_item(aid, idx)
    log.error(link)
    response.status = 301
    response.set_header("Location", link)
