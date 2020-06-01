import logging
import json
from services.restxService import create_restx_app
from services.workerService import print_result, reverse, get_alias
from flask_restx import Resource

api = create_restx_app()
ns = api.namespace('api', description='testing decoupling')

BUFFER = {}

# api endpoints
@ns.route('/process/<name>')
class Process(Resource):
    def get(self, name):
        result = {}

        # celery_task = reverse.delay(name)
        # dipatch a second task (print_result) linked by success result of a parent task (reverse)
        celery_task = reverse.s(name).apply_async(queue='linux', link=print_result.s())

        BUFFER[str(celery_task)] = celery_task
        
        result['name'] = name
        result['status'] = 'will be ready in 10 sec'
        result['taskid'] = str(celery_task)
        result['task_state'] = str(celery_task.state)
        result['scheduled'] = True
        # result['buffer_status'] = str(BUFFER)

        return json.dumps(result)

@ns.route('/status/<taskid>')
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

@ns.route('/buffer')
class GetBuffer(Resource):
    def get(self):
        result = {}
        result['result'] = str(BUFFER)
        return json.dumps(result)  

@ns.route('/alias')
class Alias(Resource):
    def get(self):
        result = {}

        celery_task = get_alias.apply_async(queue='linux')
        # dipatch a second task (print_result) linked by success result of a parent task (reverse)
        # celery_task = reverse.s().apply_async(link=print_result.s())

        BUFFER[str(celery_task)] = celery_task
        
        result['status'] = 'will be ready when powershell says'
        result['taskid'] = str(celery_task)
        result['task_state'] = str(celery_task.state)
        result['scheduled'] = True

        return json.dumps(result)