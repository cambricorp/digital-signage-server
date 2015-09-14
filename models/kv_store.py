#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Key/value store abstraction

Abstracts access to Redis data structures for our domain

All inputs/outputs are Plain Old Python Objects (POPOs)

Created by: Hugo Lima (https://github.com/hmiguellima)
"""

import logging
import datetime
from json import loads, dumps

from redis import StrictRedis

from config import settings
from utils.core import *
from consts import *


log = logging.getLogger()


class KeyValueStore(object):
    def __init__(self):
        self.data = StrictRedis(host=settings.redis.server.host,
                                port=settings.redis.server.port)
        log.debug("Connected to REDIS(%s, %s)" % (
            settings.redis.server.host, settings.redis.server.port))

    def _get_value(self, key):
        return self.data.get(key)

    def _set_value(self, key, value, seconds=None):
        self.data.set(key, value)
        if seconds is not None:
            self.data.expire(key, seconds)

    def _delete_key(self, key):
        self.data.delete(key)

    def _search_keys(self, pattern):
        return self.data.keys(pattern)

    def _get_model(self, model_pf, model_id):
        value = self._get_value(model_pf+model_id)
        if value is None:
            return None
        return Struct(loads(self._get_value(model_pf+model_id)))

    def _set_model(self, model_pf, model_id, model_value, seconds=None):
        self._set_value(model_pf + model_id,
                        dumps(model_value, default=datetime_serializer),
                        seconds)

    def _list_model(self, model_pf):
        return [Struct(loads(self._get_value(key))) for
                key in self._search_keys(model_pf+'*')]

    def _get_list_models(self, list_pf, list_id):
        return [Struct(loads(value)) for
                value in self.data.lrange(list_pf+list_id, 0, -1)]

    def _get_list_scalars(self, list_pf, list_id):
        return [value for value in self.data.lrange(list_pf+list_id, 0, -1)]

    def _pop_list_scalars(self, list_pf, list_id):
        scalars = []
        scalar = True

        while scalar:
            scalar=self.data.lpop(list_pf+list_id)
            if scalar:
                scalars += [scalar]

        return scalars

    def _push_list(self, list_pf, list_id, model_value, trim_count):
        if not isinstance(model_value, unicode):
            model_value = dumps(model_value)

        self.data.lpush(list_pf+list_id, model_value)
        self.data.ltrim(list_pf+list_id, 0, MAX_STAT_ITEMS-1)

    # Devices

    def get_device(self, mac_address):
        return self._get_model(DEVICE_PF, mac_address.replace(":","").upper())

    def set_device(self, mac_address, device):
        self._set_model(DEVICE_PF, mac_address.replace(":","").upper(), device)

    def delete_device(self, mac_address):
        self._delete_key(DEVICE_PF+mac_address.replace(":","").upper())
        self._delete_key(ASSETLIST_PF+mac_address.replace(":","").upper())

    def list_devices(self):
        return self._list_model(DEVICE_PF)

    # Assets

    def get_asset(self, guid):
        return self._get_model(ASSET_PF, guid)

    def set_asset(self, guid, asset):
        self._set_model(ASSET_PF, guid, asset)

    def delete_asset(self, guid):
        self._delete_key(ASSET_PF+guid)

    def list_assets(self):
        return self._list_model(ASSET_PF)

    # Playlists

    def get_playlist(self, name):
        return self._get_model(PLAYLIST_PF, name)

    def set_playlist(self, name, playlist):
        self._set_model(PLAYLIST_PF, name, playlist)

    def delete_playlist(self, name):
        self._delete_key(PLAYLIST_PF+name)

    def list_playlists(self):
        return self._list_model(PLAYLIST_PF)

    # Stats

    def push_stats(self, mac_address, stats):
        self._push_list(STATS_PF, mac_address, stats, MAX_STAT_ITEMS)

    def list_stats(self, mac_address):
        return self._get_list_models(STATS_PF, mac_address)

    # Alerts

    def push_alert(self, mac_address, uri):
        self._push_list(ALERTS_PF, mac_address, uri, MAX_ALERT_ITEMS)

    def list_alerts(self, mac_address):
        return self._get_list_scalars(ALERTS_PF, mac_address)

    def pop_alerts(self, mac_address):
        return self._pop_list_scalars(ALERTS_PF, mac_address)


    # Assetlists - preprocessed Playlists

    def get_assetlist(self, mac_address):
        return self._get_model(ASSETLIST_PF, mac_address.replace(":","").upper())

    def set_assetlist(self, mac_address, assetlist):
        self._set_model(ASSETLIST_PF, mac_address.replace(":","").upper(), assetlist)

    def delete_assetlist(self, mac_address):
        self._delete_key(ASSETLIST_PF+mac_address.replace(":","").upper())

    def list_assetlists(self):
        assetlists = self._list_model(ASSETLIST_PF)
        for assetlist in assetlists:
            assetlist['timestamp'] = datetime.datetime.now().timestamp()
        return assetlists

    #MEO List with expiration

    def get_meolist(self, playlist_name, index):
        return self._get_model(MEOKANAL_PF, playlist_name.replace(":","") + "_" + str(index))

    def set_meolist(self, playlist_name, index, seconds, meolist):
        self._set_model(MEOKANAL_PF, playlist_name.replace(":","") + "_" + str(index), meolist, seconds)
