#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Twitter pseudo-API

Created by: Rui Carmo (https://github.com/rcarmo)
"""

import os, sys, logging, time, datetime, calendar
from json import dumps, loads, JSONEncoder
from bottle import route, get, put, post, delete, request, response, abort
from controllers.feeds import FeedController
from decorators import jsonp, cache_results, timed, redis_cache, cache_control
import feedparser

class ExtendedEncoder(JSONEncoder):
    """JSON encoder that knows how to serialize some extra types"""

    def default(self, item):
        if isinstance(item, datetime.datetime):
            return calendar.timegm(item.utctimetuple())
        if isinstance(item, datetime.date):
            return time.mktime(item.timetuple())
        if isinstance(item, time.struct_time):
            return calendar.timegm(item)
        return JSONEncoder.default(self, item)
    
prefix = '/feeds'
log = logging.getLogger()                                                      
c = FeedController()

@get(prefix + '/time')
@timed
@jsonp
def get_server_time():
    """Returns the server clock (we don't trust the client clocks)"""
    return {"server_time":int(time.time() * 1000)}
    return {"server_time":int(calendar.timegm(datetime.datetime.utcnow().utctimetuple()) * 1000)}


@get(prefix + '/twitter')
@timed
@cache_control(60)
@jsonp
def get_twitter_data():
    """Returns the latest twitter data"""

    res = c.twitter_feed
    if not res:
        abort(204, "No content")
        return None

    response.content_type = "application/json"
    return res

@get(prefix + '/rss/<feed_name>')
@timed
@cache_results(60)
@cache_control(60)
@jsonp
def get_rss_feed(feed_name):
    try:
        feed_response = c.get_feed(feed_name)
    
        response.status = feed_response['status']
        
        if feed_response['status'] == 200:
            # SAPO Fotos gives us the wrong content-type, so testing for text/xml is kind of pointless
            if 'text/' in feed_response['content-type']:
                encoder = ExtendedEncoder()
                
                feed_response['data'] = encoder.encode(feedparser.parse(feed_response['data']))  
        
            # return a dict so that Bottle can handle this for us
            return loads(feed_response['data'])
    except Exception as ex:
        abort(404, "Feed not found: %s" % ex)
        log.error(ex)
    
