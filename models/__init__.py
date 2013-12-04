#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Rui Carmo <rui.carmo@co.sapo.pt>
Description: Data models for the Codebits digital signage system.
License: MIT (see LICENSE for details)
"""

import os, sys, logging, datetime, time
from peewee import *

log = logging.getLogger()

from config import settings

if settings.storage.db.engine == 'sqlite3':
    db = SqliteDatabase(settings.storage.db.filename, threadlocals=True)
elif settings.storage.db.engine == 'postgres':
    db = PostgresqlDatabase(settings.storage.db.name)
    db.connect()
else:
    print "Unknown database engine"
    sys.exit(2)


class CustomModel(Model):
    """Binds the database to all our models"""
    class Meta:
        database = db


class Device(CustomModel):
    """Represents a client device"""

    mac_address     = CharField(primary_key=True,unique=True) 
    ip_address      = CharField(null=False) 
    real_ip_address = CharField(null=False) 
    name            = CharField(null=False, default="Unnamed", max_length=32)
    active          = BooleanField(default=False)
    version         = CharField(null=True)
    last_seen       = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (
            (('ip_address',), True),
            (('version',), False),
            (('last_seen',), False),
        )
        order_by = ('-last_seen',)


class Stats(CustomModel):
    """Represents client device statistics"""

    mac_address = CharField(null=False) 
    last_seen   = DateTimeField(default=datetime.datetime.now)
    cpu_freq    = FloatField(null=False)
    cpu_temp    = FloatField(null=False)
    cpu_usage   = FloatField(null=False)
    browser_ram = FloatField(null=False)

    class Meta:
        indexes = (
            (('last_seen',), False),
        )
        order_by = ('-last_seen',)


class Queue(CustomModel):
    """Represents queued instructions for a client device"""

    scheduled   = DateTimeField(primary_key=True,unique=True,default=datetime.datetime.now)
    mac_address = CharField(null=False)
    action      = CharField(null=False)
    data        = CharField(null=True)
    sent        = BooleanField(default=False)

    class Meta:
        indexes = (
            (('mac_address',), False),
        )
        order_by = ('-scheduled',)
        
        
class ServerStats(CustomModel):
    """Represents server statistics"""
    
    when        = DateTimeField(primary_key=True,unique=True,default=datetime.datetime.now)
    rx_bytes    = FloatField(null=False)
    tx_bytes    = FloatField(null=False)
    cpu_usage   = FloatField(null=False)

    class Meta:
        order_by = ('-when',)


class BaseController:
    """A base controller class that knows about our database"""

    def __init__(self):
        db.connect()

    def __del__(self):
        try:
            db.close()
        except Exception, e:
            log.debug("Error closing database connection: %s" % e)
            pass


def setup():
    """Setup database tables"""
    models = [ServerStats, Queue, Device, Stats]
    for m in models:
        m.create_table(skip_if_existing)
    if settings.db.back_end == 'sqlite3':
        db.execute_sql('PRAGMA journal_mode=WAL')