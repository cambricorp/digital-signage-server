#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Video tasks

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
from .generic import reaper

log = logging.getLogger()

r = Redis(settings.celery.broker_url)


def _lock_files(self):
    """Returns existing/extant X11 lock files -- adapted from xvfbwrapper"""

    tmpdir = '/tmp'
    pattern = '.X*-lock'
    names = fnmatch.filter(os.listdir(tmpdir), pattern)
    ls = [os.path.join(tmpdir, child) for child in names]
    ls = [p for p in ls if os.path.isfile(p)]
    return ls


def get_free_display():
    """Finds a free X11 display number -- adapted from xvfbwrapper"""

    ls = [int(x.split('X')[1].split('-')[0]) for x in _lock_files()]
    min_display_num = 1000
    if len(ls):
        display_num = max(min_display_num, max(ls) + 1)
    else:
        display_num = min_display_num
    random.seed()
    display_num += random.randint(0, 100)
    return display_num


@celery.task(retries=3)
def record(url, length, ttl=0, uuid = None):
    """Record a video segment of a given page"""

    if not uuid:
        uuid = uuid5(NAMESPACE_URL, url)

    result_filename = uuid_path("%dx%d-%ds.jpg" % (width, height, length), root=settings.store.images, id=uuid)
    # TODO: check if file already exists, is valid and whether or not it needs updating

    display = get_free_display()

    xvfb = subprocess.Popen(settings.xvfb.cli % (display, width, height), stdout=PIPE, stderr=PIPE)
    time.sleep(0.5) # let it settle a bit
    res = xvfb.poll()
    if res is None:
        os.environ["DISPLAY"] = ":%d" % display
    else:
        raise RuntimeError("Xvfb failed to start, returned %d" % res)

    ih, movie_filename = tempfile.mkstemp(suffix='.mp4')
    os.close(ih)

    # TODO: launch uzbl, blank it, and prepare to record

    cvlc = subprocess.Popen(settings.vlc.cli % (0, length, movie_filename), stdout=PIPE, stderr=PIPE)
    reaper.delay([xvfb.pid, cvlc.pid], length + 1)
    cvlc.wait()

    shutil.rename(movie_filename, result_filename)
    return result_filename
