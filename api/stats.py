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

r = Redis(settings.celery.broker_url)

max_data_points = 

prefix = api.prefix + '/stats'

# Collection URI - List
@get(prefix)
def list():
    abort(501,'Not Implemented')
    

# Collection URI - Replace entire collection
@put(prefix)
def replace():
    abort(405,'Not Allowed')


# Collection URI - Add item to collection
@check_valid_beacon
@post(prefix)
def append():
	data = Struct(request.forms)
	data.when = time.time()
	count = r.lpush("stats:%s" % data.mac_address, json.dumps(data))
	limit = r.get("config:max_data_points")
	if limit and count > limit:
		r.ltrim("stats:%s" % data.mac_address, 0, limit)


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