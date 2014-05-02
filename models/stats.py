'''
Created on Mar 14, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''


from utils.core import Struct

class Stats(Struct):
    """
    Represents a playlist asset
    """

    def __init__(self, date_time, state, debug_message):
        value = {
                 'date_time': date_time,
                 'state': state,
                 'debug_message': debug_message
                }

        super(Stats, self).__init__(value)
