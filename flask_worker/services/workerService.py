import os
import time
from app_library import send_teams_message
from services.celeryService import make_single_celery

linux = make_single_celery()

# celery tasks
@linux.task(name='reverse')
def reverse(word):
    time.sleep(10)
    return word[::-1]

@linux.task(name='print_result') # dispatcher for reverse task
def print_result(result):
    # send_teams_message('task dispatcher')
    return result[::-1]

@linux.task(bind=True, name='powershell') 
def get_alias(self):
    SCRIPT = 'get_alias.ps1'
    PATH = '../../scripts/'
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