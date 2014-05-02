'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

from utils.core import Struct

class Playlist(Struct):
    """
    Represents a playlist (ordered list of assets)
    """

    def __init__(self, name, description, assets_list):
        value = {
                 'name': name,
                 'description': description,
                 'assets': assets_list
                }

        super(Playlist, self).__init__(value)
