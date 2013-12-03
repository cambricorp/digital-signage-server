#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Worker tasks

Created by: Rui Carmo
"""

from __future__ import absolute_import

import os, sys, re, logging, time, subprocess, json, tempfile

sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../lib'))

from config import settings
from tasks.celery import celery.task as task
from utils.core import Struct, path_for
from utils.filekit import uuid_path
from uuid import uuid5
from redis import StrictRedis as Redis
from time import time

log = logging.getLogger()

r = Redis(settings.celery.broker_url)

@task(retries=3)
def snapshot_set(url, ttl=0, uuid = None):
    if not uuid:
        uuid = str(uuid5("url", uri))

    result = []
    for s in settings.phantom.sizes:
        width, height = s.split('x')
        snapshot.delay(url, width, height, ttl, uuid)
    return result

@task(retries=3)
def snapshot(url, width, height, ttl, uuid):
    result_filename = uuid_path("%s.jpg" % s, settings.store.images, uuid)
    #TODO: check if file already exists, is valid and whether or not it needs updating
    ih, image_filename = tempfile.mkstemp(suffix='.png')
    subprocess.call([settings.phantom.path,'--ignore-ssl-errors=yes','--ssl-protocol=any',path_for('etc/snap.js'),url,image_filename, width, height, settings.phantom.timeout)
    os.close(ih)
    #TODO: validate output file format
    subprocess.call(settings.magick.args % (settings.magick.path, image_filename, result_filename), shell=True)
    os.unlink(image_filename)
    return result_filename
