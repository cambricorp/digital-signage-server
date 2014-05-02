from __future__ import absolute_import
from operator import sub

import os, sys, re, logging, calendar, datetime, json, traceback
from redis import StrictRedis as Redis
from random import shuffle
import hashlib

sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../lib'))

from config import settings
from models.consts import *
from tasks.celery import celery
from utils.core import *

log = logging.getLogger()

from controllers.playlists import PlaylistController
from controllers.assetlist import AssetlistController
from controllers.devices import DeviceController
from controllers.assets import AssetController

plControl = PlaylistController()
alControl = AssetlistController()
dvControl = DeviceController()
astControl = AssetController()

#novos parametros para termos suffle e limite de items nas subplaylists
def process_assets(name, pListAssets, visited):
    playlist = []
    for idx, assetList in enumerate(pListAssets):
        info = astControl.get_asset(assetList["guid"])
        if not info:
            continue
        if info.type == 'playlist':
            pl = plControl.get_playlist(info.uri.replace('playlist://', ''))
            if pl is not None and pl.name not in visited:
                sub_playlist = process_assets(pl.name, pl.assets, visited + [pl.name])
                # tratamento do shuffle e limitacao dos items nas subplaylists
                if info.shuffle:
                    shuffle(sub_playlist)
                if info.how_many and int(info.how_many) > 0:
                    sub_playlist = sub_playlist[:int(info.how_many)]
                # fim do tratamento do shuffle e limitacao dos items nas subplaylists
                playlist.extend(sub_playlist)
        if info.type == 'web' or info.type == 'video':
            playlist.append({'guid': info.guid, 'type': info.type, 'duration_secs': int(info.duration_secs), 'uri': info.uri})
        # removed meokanal code
    return playlist

@celery.task
def refresh_assetlists():
    try:
        playlists = plControl.get_all_playlists()
        devices = dvControl.get_all_devices()
        playlistByName = {}
        for playlist in playlists:
            playlistByName[playlist.name] = process_assets(playlist.name, playlist.assets, [playlist.name])
        plWithGuid = {}
        for playlist, assets in playlistByName.iteritems():
            guids = []
            for asset in assets:
                guids.append(asset["guid"])
            plWithGuid[playlist] = {"assets": assets, "guid": hashlib.sha256("".join(guids)).hexdigest()}
        for device in devices:
            if device["playlist"] in plWithGuid:
                alControl.set_assetlist(device["mac_address"], plWithGuid[device["playlist"]])
    except Exception as e:
        log.error(e)
        traceback.print_exc()
