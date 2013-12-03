#celery worker --app=tasks.celery --concurrency=1 -P gevent -l debug
celery worker --app=tasks.celery --concurrency=10 -P gevent -l debug
# disable info logs in production
# celery worker --app=tasks.celery --autoscale=24,4
