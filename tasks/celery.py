#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Celery setup

Created by: Rui Carmo
"""

from __future__ import absolute_import

import os, sys, celery
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../lib'))

from config import settings
from datetime import timedelta

celery = celery.Celery('tasks.celery',
    broker  = settings.celery.broker_url,
    backend = settings.celery.result_backend,
    # task modules to load onto Celery
    include=['tasks.twitter', 'tasks.assetlist'])

celery.conf.update(
    CELERY_ENABLE_UTC = True,
    CELERY_TIMEZONE = "Europe/Lisbon",
    CELERY_TASK_RESULT_EXPIRES=1000,
    CELERY_ANNOTATIONS = {
        "*": { "rate_limit": settings.celery.rate_limit }
    },
    CELERYBEAT_SCHEDULE = {
        "check-twitter": {
            "task": "tasks.twitter.perform_query",
            "schedule": timedelta(seconds=settings.twitter.interval),
            "args": (settings.twitter.search_query,
                     settings.twitter.geocode,
                     settings.twitter.limit)
        },
        "check-assetlist": {
            "task": "tasks.assetlist.refresh_assetlists",
            "schedule": timedelta(seconds=settings.assetlist.interval)
        }
    }
)

if __name__ == '__main__':
    celery.start()
