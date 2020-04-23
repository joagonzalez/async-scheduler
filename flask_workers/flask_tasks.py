from celery import Celery
import time

app = Celery('flask_tasks', backend = 'rpc://',  broker='pyamqp://guest@localhost//')

@app.flask_tasks
def add(x, y):
    time.sleep(10)
    return x + y

@app.flask_tasks
def wait_seconds(seconds):
    time.sleep(seconds)