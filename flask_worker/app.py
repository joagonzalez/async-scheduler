from flask import Flask
from flask_restx import Api, Resource
from celery import Celery
from flask_celery import make_celery
from app_library import *

# configure logger
setup_logging(default_path='logging.json')
logger = logging.getLogger(CONFIG['FLASK']['LOGGER']) # use logger instead of loggin

# congure flask app
app_flask = Flask(__name__)
app_flask.config['CELERY_BROKER_URL'] = CONFIG['CELERY']['CELERY_BROKER_URL']
app_flask.config['CELERY_BACKEND'] = CONFIG['CELERY']['CELERY_BACKEND']
app_flask.config['ACCEPT_CONTENT'] = CONFIG['CELERY']['ACCEPT_CONTENT']
app_flask.config['TASK_SERIALIZER'] = CONFIG['CELERY']['TASK_SERIALIZER']

# configure celery
celery = make_celery(app_flask)

# configure flask restx
app = Api(app=app_flask, version=CONFIG['RESTX']['VERSION'], title=CONFIG['RESTX']['TITLE'], description=CONFIG['RESTX']['DESCRIPTION'])

BUFFER = {}

# api endpoints
@app.route('/process/<name>')
class Process(Resource):
    def get(self, name):
        result = {}

        # celery_task = reverse.delay(name)
        # dipatch a second task (print_result) linked by success result of a parent task (reverse)
        celery_task = reverse.s(name).apply_async(link=print_result.s())

        BUFFER[str(celery_task)] = celery_task
        
        result['name'] = name
        result['status'] = 'will be ready in 10 sec'
        result['taskid'] = str(celery_task)
        result['task_state'] = str(celery_task.state)
        result['scheduled'] = True
        # result['buffer_status'] = str(BUFFER)

        return json.dumps(result)

@app.route('/status/<taskid>')
class Status(Resource):
    def get(self, taskid):
        result = {}
        if taskid in BUFFER:
            result['status'] = str(BUFFER[taskid].state)
            if result['status'] == 'SUCCESS':
                result['result'] = str(BUFFER[taskid].get(propagate=False))
                notification = '<b>Task ID: </b>' + taskid + ': ' + ' - <b>Status: </b>' + result['status'] + ' - <b>Result: </b>' + result['result']
                result['notification'] = str(send_teams_message(notification))
            else:
                result['result'] = 'Not ready'
        else:
            result['status'] = 'Task not in buffer'
            result['result'] = 'Not ready'  
        return json.dumps(result) 

@app.route('/buffer')
class GetBuffer(Resource):
    def get(self):
        result = {}
        result['result'] = str(BUFFER)
        return json.dumps(result)  

@app.route('/alias')
class Alias(Resource):
    def get(self):
        result = {}

        celery_task = get_alias.delay()
        # dipatch a second task (print_result) linked by success result of a parent task (reverse)
        # celery_task = reverse.s().apply_async(link=print_result.s())

        BUFFER[str(celery_task)] = celery_task
        
        result['status'] = 'will be ready when powershell says'
        result['taskid'] = str(celery_task)
        result['task_state'] = str(celery_task.state)
        result['scheduled'] = True

        return json.dumps(result)

# celery tasks
@celery.task(name='app.reverse')
def reverse(word):
    time.sleep(10)
    return word[::-1]

@celery.task(name='app.print_result') # dispatcher for reverse task
def print_result(result):
    # send_teams_message('task dispatcher')
    return result[::-1]

@celery.task(bind=True, name='app.powershell') 
def get_alias(self):
    SCRIPT = 'alias.ps1'
    PATH = 'scripts/'
    CMD = 'powershell ../' + PATH + SCRIPT
    MESSAGE = []
    result = os.system(CMD + ' >> output_' + str(self.request.id) + '.txt')

    f = open('output_' + str(self.request.id) + '.txt')
    for line in f:
        MESSAGE.append('\n' + line)

    f.close()

    os.system('powershell rm output_' + str(self.request.id) + '.txt')

    send_teams_message('task id:' + str(self.request.id) + '\ndump: ' + str(MESSAGE[:80]))
    return str(result)

if __name__ == '__main__':
    create_app(app_flask, logger)