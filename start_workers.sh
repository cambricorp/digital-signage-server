#!/bin/sh
# -B option turns on scheduler

. ../digital-signage-env/bin/activate

#exec celery worker -B --app=tasks.celery --concurrency=1 -P gevent -l debug
exec celery worker -E -B --beat --app=tasks.celery --concurrency=10 -l info
# disable info logs in production
# exec celery worker -B --app=tasks.celery --autoscale=24,4
