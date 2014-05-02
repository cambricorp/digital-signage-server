'''
Created on Mar 28, 2014

@author: brsantos
'''

from utils.core import Struct

class Assetlist(Struct):
    """
    Represents a assetlist (ordered list of assets preprocessed to each device)
    """
    
    def __init__(self, mac_address, assets):
        value = {
                 'mac_address': mac_address,
                 'info': assets
                }

        super(Assetlist, self).__init__(value)
        