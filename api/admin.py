#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Administration backend API

Created by: Hugo Lima (https://github.com/hmiguellima)
"""

import os, sys, logging, time, copy
from json import dumps, loads
from bottle import route, get, put, post, delete, request, response, abort
import api
from controllers.assets import AssetController
from controllers.devices import DeviceController
from controllers.playlists import PlaylistController
from controllers.stats import StatsController
from controllers.alerts import AlertsController
import uuid
from aaa import authorize 
from decorators import timed, cache_control

log = logging.getLogger()
devices = DeviceController()
assets = AssetController()
playlists = PlaylistController()
stats = StatsController()
alerts = AlertsController()

prefix = api.prefix + '/admin'

# Devices

@get(prefix + '/device/list')
@authorize()
@timed
@cache_control(0)
def list_devices():
    return {'devices': sorted(devices.get_all_devices(), key=lambda device: device.name.lower())}

@post(prefix + '/device/detail/<mac_address>')
@authorize()
@timed
def create_device(mac_address):
    if devices.get_device(mac_address) is not None:
        raise Exception('A device with that mac address exists')

    device = {}
    device.update(request.json)
    device['mac_address'] = mac_address
    
    devices.set_device(**device)     

@put(prefix + '/device/detail/<mac_address>')
@authorize()
@timed
def update_device(mac_address):
    print mac_address
    if devices.get_device(mac_address) is None:
        raise Exception('A device with that mac address doesn\'t exist')

    device = {}
    device.update(request.json)
    device['mac_address'] = mac_address
    
    devices.set_device(**device)     

@delete(prefix + '/device/detail/<mac_address>')
@authorize()
@timed
def delete_device(mac_address):
    devices.delete_device(mac_address)
    
# Assets

@get(prefix + '/asset/list')
@authorize()
@timed
@cache_control(0)
def list_assets():
    return {'assets': sorted(assets.get_all_assets(), key=lambda asset: asset.description.lower())}

@post(prefix + '/asset/detail')
@authorize()
@timed
def create_asset():
    req = {}
    json = request.json
    for key in json.keys():
        req[key] = json[key]
    req["guid"] = str(uuid.uuid4())
    assets.set_asset(**req)
    return req

@post(prefix + '/asset/detail/<guid>')
@authorize()
@timed
def update_asset(guid):
    req = request.json
    if "guid" not in request.json:
        req = {}
        json = request.json
        for key in json.keys():
            req[key] = json[key]
        req["guid"] = guid
    
    assets.set_asset(**req)

@delete(prefix + '/asset/detail/<guid>')
@authorize()
@timed
def delete_asset(guid):
    assets.delete_asset(guid)
    
# Playlists

@get(prefix + '/playlist/list')
@authorize()
@timed
@cache_control(0)
def list_playlists():
    return {'playlists': playlists.get_all_playlists()}

@post(prefix + '/playlist/detail/<name>')
@authorize()
@timed
def create_playlist(name):
    if playlists.get_playlist(name) is not None:
        raise Exception('A playlist with that name exists')

    playlist = {}
    playlist.update(request.json)
    playlist['name'] = name
    
    playlists.set_playlist(**playlist)
    
@put(prefix + '/playlist/detail/<name>')
@authorize()
@timed
def update_playlist(name):
    if playlists.get_playlist(name) is None:
        raise Exception('A playlist with that name doesn\'t exist')

    playlist = {}
    playlist.update(request.json)
    playlist['name'] = name
    
    playlists.set_playlist(**playlist)

@delete(prefix + '/playlist/detail/<name>')
@authorize()
@timed
def delete_playlist(name):
    playlists.delete_playlist(name)

# Statistics

@get(prefix + '/stats/device/<mac_address')
@authorize()
@timed
@cache_control(0)
def list_stats(mac_address):
    return {'stats': stats.list_stats(mac_address)}

# Alerts

@post(prefix + '/alerts/batch')
@authorize()
@timed
def send_alerts():
    alerts.push_alert(**request.json)
    
@get(prefix + '/alerts/templates')
@authorize()
@timed
def list_alert_templates():
    return {'templates': alerts.list_templates()}
