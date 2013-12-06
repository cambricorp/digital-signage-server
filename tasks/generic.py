#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic tasks

Created by: Rui Carmo
"""

from __future__ import absolute_import

import os, sys, re, logging, time, subprocess, json, tempfile

sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../lib'))

@celery.task
def reaper(pids, delay):
    time.sleep(delay)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
            log.warn("Killed %d, was apparently stuck." % pid)
        except Exception as e:
            log.debug("Could not kill %d: %s" % (pid, e))
