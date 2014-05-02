'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

from utils.core import Struct

class Device(Struct):
    """
    Represents a plasma client device
    """

    def __init__(self, mac_address, ip_address, name, active, version, playlist):
        value = {
                 'mac_address': mac_address,
                 'ip_address': ip_address,
                 'name': name,
                 'active': active,
                 'version': version,
                 'playlist': playlist
                }

        super(Device, self).__init__(value)
