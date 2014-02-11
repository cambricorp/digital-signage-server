#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Template file for an API branch

Created by: Rui Carmo
"""

import os, sys, logging, json, time
from bottle import route, get, put, post, delete, request, response, abort

log = logging.getLogger()

import api
from config import settings
from redis import StrictRedis as Redis
from utils.core import Struct
from .decorators import check_valid_beacon

r = Redis(**settings.redis.server)

prefix = api.prefix + '/metrics'

# Collection URI - List
@get(prefix)
def list_data():
    """

    /api/v1/metrics

    Returns the set of clients and metrics currently being tracked.
    """
    return { 
        "clients": r.smembers("metrics:_clients"), 
        "metrics": r.smembers("metrics:_labels") 
    }
    

# Collection URI - Replace entire collection
@put(prefix)
def replace():
    abort(405,'Not Allowed')


# Collection URI - Add item to collection
@post(prefix)
@check_valid_beacon
def add_data_point():
    """

    /api/v1/metrics

    Adds a data point to the various metrics. Requires a valid MAC address and IP address, tracks:

    * `cpu_temp`
    * `cpu_usage`
    * `browser_ram` - deprecated
    * `free_ram`
    * `free_disk`
    * `tx_bytes`
    * `rx_bytes`
    """

    types = {
        'playlist'    : str,
        'mac_address' : str,
        'ip_address'  : str,
        'cpu_freq'    : int,
        'cpu_temp'    : float,
        'cpu_usage'   : int,
        'browser_ram' : int,
        'free_ram'    : int,
        'free_disk'   : int,
        'uptime'      : int,
        'tx_bytes'    : int,
        'rx_bytes'    : int,        
    }

    data = Struct(request.forms)

    # enforce typing - we can't do that on a request.forms dict
    for field in types:
        if field in data:
            data[field] = types[field](data[field])
    
    # add a timestamp    
    data.when = time.time()
    log.debug(data)

    # store current status
    r.set("status:%s" % data.mac_address, json.dumps(data))
    r.sadd("metrics:_clients", data.mac_address)

    limit = r.get("config:max_data_points")

    # store each interesting field in its own (capped) list
    stored = []
    for interesting in ['cpu_temp','cpu_usage','browser_ram','free_ram','free_disk','tx_bytes','rx_bytes']:
        if interesting in request.forms:
            count = r.lpush("metrics:%s:%s" % (interesting, data.mac_address), json.dumps({"t": data.when, "v": data[interesting]}))
            r.sadd("metrics:_labels", interesting)
            stored.append(interesting)
            if limit and count > limit:
                r.ltrim("metrics:%s" % data.mac_address, 0, limit)
    # tell the client what we stored
    return {"stored": stored}

# Collection URI - Delete entire collection
@delete(prefix)
def remove():
    abort(405,'Not Allowed')


# Element URI - Retrieve element
@get(prefix + '/<id>')
def element(id):
    abort(501,'Not Implemented')


# Element URI - Replace or create element
@put(prefix + '/<id>')
def replace(id):
    abort(501,'Not Implemented')


# Element URI - Create new named element (doesn't make sense in most cases)
@post(prefix + '/<id>')
def unused(id):
    abort(501,'Not Implemented')


# Element URI - Patch existing named element (returns 204 No content on success as per RFC 5789)
@route(prefix + '/<id>', method='PATCH')
def unused(id):
    abort(501,'Not Implemented')

# Element URI - Delete element
@delete(prefix + '/<id>')
def delete(id):
    abort(501,'Not Implemented')
