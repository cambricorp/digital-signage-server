#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main application script

Created by: Rui Carmo
"""

import os, sys, logging

# Make sure our bundled libraries take precedence
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib'))

import utils, bottle
from config import settings
from beaker.middleware import SessionMiddleware
#from gevent import monkey

#monkey.patch_all()

app = SessionMiddleware(bottle.app(), settings.http.session_opts)
log = logging.getLogger()

@bottle.error()
def error_handler(e):
    return str(e.exception)

if __name__ == "__main__":

    if settings.reloader:
        if 'BOTTLE_CHILD' not in os.environ:
            log.debug('Using reloader, spawning first child.')
        else:
            log.debug('Child spawned.')

    if not settings.reloader or ('BOTTLE_CHILD' in os.environ):
        log.info("Setting up application.")
        import api, routes, controllers
        log.info("Serving requests.")

    bottle.run(
        port     = settings.http.port, 
        host     = settings.http.bind_address, 
        debug    = settings.debug,
        reloader = settings.reloader,
        app      = app,
        server   = settings.http.server,
        **settings.http.server_options 
    )
else:
    application = app
