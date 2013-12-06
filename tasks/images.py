#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image tasks

Created by: Rui Carmo
"""

from __future__ import absolute_import

import os, sys, re, logging, time, subprocess, json, tempfile

sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../lib'))

from config import settings
from tasks.celery import celery
from utils.core import Struct
from utils.filekit import uuid_path, path_for
from uuid import uuid5, NAMESPACE_URL
from redis import StrictRedis as Redis
from time import time

log = logging.getLogger()

r = Redis(settings.celery.broker_url)

@celery.task(retries=3)
def snapshot_set(url, ttl=0, uuid = None):
    if not uuid:
        uuid = uuid5(NAMESPACE_URL, url)

    result = []
    for s in settings.phantom.sizes:
        width, height = map(int,s.split('x'))
        log.debug(s)
        result.append(snapshot.delay(url, width, height, ttl, uuid))
    return result


@celery.task(retries=3)
def snapshot(url, width, height, ttl, uuid):
    result_filename = uuid_path("%dx%d.jpg" % (width, height), root=settings.store.images, id=uuid)
    # TODO: check if file already exists, is valid and whether or not it needs updating
    ih, image_filename = tempfile.mkstemp(suffix='.png')
    os.close(ih)
    # TODO: set up reaper
    subprocess.call([settings.phantom.path,'--ignore-ssl-errors=yes','--ssl-protocol=any',path_for('etc/snap.js'),url, image_filename, str(width), str(height), str(settings.phantom.timeout)])
    # TODO: validate output file format
    try:
        os.makedirs(os.path.dirname(result_filename))
    except OSError, e:
        if "exists" not in str(e).lower():
            raise
    subprocess.call(settings.imagemagick.args % (settings.imagemagick.convert, image_filename, result_filename), shell=True)
    os.unlink(image_filename)
    return result_filename
