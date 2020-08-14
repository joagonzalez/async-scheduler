from celery import Celery 
from settings import *

def make_single_celery():
    celery = Celery('base', backend=CONFIG['CELERY']['CELERY_BACKEND'],
                    broker=CONFIG['CELERY']['CELERY_BROKER_URL'], accept_content=CONFIG['CELERY']['ACCEPT_CONTENT'], 
                    task_serializer=CONFIG['CELERY']['TASK_SERIALIZER'], celery_accept_content=CONFIG['CELERY']['ACCEPT_CONTENT'])
    return celery
