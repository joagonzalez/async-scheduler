import sys
import time
from settings import *
from flask import Flask
from flask_celery import make_celery

# Flask app definition and config
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_BACKEND'] = CELERY_BACKEND

# Celery app definition and config
celery = make_celery(app)

@app.route('/process/<name>')
def process(name):
    return name

@celery.flask_tasks
def add(x, y):
    time.sleep(10)
    return x + y

if __name__ == '__main__':
    app.run(debug=True)