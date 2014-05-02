'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

import os, sys, logging
from json import loads
from models.device import Device
from models.asset import Asset
from models.playlist import Playlist

log = logging.getLogger()

from base import BaseController

class PlaylistController(BaseController):
    def __init__(self):
        super(PlaylistController, self).__init__()

    def get_playlist(self, name):
        return self.kv.get_playlist(name)

    def get_all_playlists(self):
        return self.kv.list_playlists()

    def set_playlist(self, name, description, assets):
        self.kv.set_playlist(name, Playlist(name, description, assets))

    def get_playlist(self, name):
        return self.kv.get_playlist(name)

    def delete_playlist(self, name):
        self.kv.delete_playlist(name)
