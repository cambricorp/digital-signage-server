#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Static routes

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import os, sys, logging
from bottle import route, static_file
from aaa import auth

log = logging.getLogger()

@route('/')
@auth()
def index():
    """Index file handler"""
    return static_file('index.html', root='static')

@route('/<path:path>')
def send_static(path):
    """Static file handler"""
    return static_file(path, root='static')

