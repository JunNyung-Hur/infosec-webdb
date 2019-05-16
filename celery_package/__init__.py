from celery import Celery
import settings, sys, os

def make_celery():
    celery = Celery(settings.APP_NAME, broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
    celery.conf.update(
        broker_url=settings.CELERY_BROKER_URL,
        result_backend=settings.CELERY_RESULT_BACKEND,
        task_ignore_result=False
    )

    return celery

if __name__ == 'celery_package':
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
    celery = make_celery()
    celery.autodiscover_tasks(['celery_package.views'])