import sys
import time
import json
from flask import Flask
from celery import Celery
from flask_celery import make_celery
from settings import *

#congure flask app
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_BACKEND'] = CELERY_BACKEND

#configure celery
celery = make_celery(app)

BUFFER = {}

@app.route('/process/<name>')
def process(name):
    result = {}

    celery_task = reverse.delay(name)

    BUFFER[str(celery_task)] = reverse.delay(name)
    
    result['name'] = name
    result['status'] = 'will be ready in 10 sec'
    result['taskid'] = str(celery_task)
    result['task_state'] = str(celery_task.state)
    result['scheduled'] = True
    result['buffer_status'] = str(BUFFER)

    return json.dumps(result)

@app.route('/status/<taskid>')
def status(taskid):
    result = {}
    if taskid in BUFFER:
        result['status'] = str(BUFFER[taskid].state)
        if result['status'] == 'SUCCESS':
            result['result'] = str(BUFFER[taskid].get(propagate=False))
        else:
            result['result'] = 'Not ready'
    else:
        result['status'] = 'Task not in buffer'
        result['result'] = 'Not ready'  
    return json.dumps(result) 

# defino celery task en archivo app funcion add
@celery.task(name='app.reverse')
def reverse(word):
    time.sleep(10)
    return word[::-1]

if __name__ == '__main__':
    app.run(debug=DEBUG)