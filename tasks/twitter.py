#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Twitter API crawler

Created by: Rui Carmo
"""

from __future__ import absolute_import

import os, sys, re, logging, calendar, datetime, json
from redis import StrictRedis as Redis

sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../lib'))

from config import settings
from models.consts import *
from tasks.celery import celery

import tweepy # our custom version with proxy support
from controllers.feeds import FeedController

log = logging.getLogger()

def get_api(twitter):
    """Return a Twitter API object"""

    auth = tweepy.OAuthHandler(twitter.consumer_key, twitter.consumer_secret)
    auth.set_access_token(twitter.access_key, twitter.access_secret)
    return tweepy.API(auth_handler=auth, secure=True, retry_count=3,
                      proxy_host=settings.twitter.proxy_host,
                      proxy_port=settings.twitter.proxy_port)


class ExtendedEncoder(json.JSONEncoder):
    """JSON encoder that knows how to serialize some of our models"""

    def default(self, item):
        if isinstance(item, datetime.datetime):
            return calendar.timegm(item.utctimetuple())
        if isinstance(item, datetime.date):
            return time.mktime(item.timetuple())
        if isinstance(item, tweepy.API):
            return "1.1"
        if isinstance(item, tweepy.models.Status):
            return item.__dict__
        if isinstance(item, tweepy.models.Place):
            return "<geotag>"
        if isinstance(item, tweepy.models.User):
            return item.__dict__
        return json.JSONEncoder.default(self, item)

@celery.task
def perform_query(query_string, geocode = None, max_results = 25):
    """Perform a Twitter query and place an enriched JSON buffer in Redis"""

    api = get_api(settings.twitter)
    r = Redis(settings.redis.server.host, settings.redis.server.port)
    log.debug("Performing Twitter query %s" % query_string)
    res = api.search(query_string, rpp = max_results, geocode = geocode)
    statuses = [s for s in res]
    log.debug("Got %d results" % len(statuses))
    # Now serialize the enriched output using our custom encoder
    data = json.dumps({"count": len(statuses), "statuses":statuses}, cls=ExtendedEncoder)
    # And store it into Redis if we have a valid result
    if len(statuses):
        c = FeedController()
        c.twitter_feed = data
    return data
