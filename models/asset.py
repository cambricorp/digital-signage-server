'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

from utils.core import Struct

class Asset(Struct):
    """
    Represents a playlist asset
    """

    def __init__(self, uri, guid=None, description=None, uri_type=None, duration_secs=None, pin=None, how_many=None, shuffle=None):
        value = {
                 'uri': uri,
                }

        if guid is not None:
            value['guid'] = guid

        if description is not None:
            value['description'] = description

        if uri_type is not None:
            value['type'] = uri_type

        if duration_secs is not None:
            value['duration_secs'] = int(duration_secs)

        if pin is not None:
            value['pin'] = pin

        if how_many is not None:
            value['how_many'] = how_many

        if shuffle is not None:
            value['shuffle'] = shuffle

        super(Asset, self).__init__(value)
