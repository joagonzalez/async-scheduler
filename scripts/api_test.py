import os
import time
import sys
import requests

HOST = 'http://newcos-sandbox-04.smq.net'
PORT = 5000
ENDPOINT = 'alias'
WORD = str(sys.argv[1])
ERROR_BUFFER = 0
TOTAL_BUFFER = 0
TIME = 3
while True:
    URL = HOST + ':' + str(PORT) + '/' + ENDPOINT #+ '/' + WORD 
    result = requests.get(URL)
    print(result)
    TOTAL_BUFFER += 1
    if result.status_code == 500:
        ERROR_BUFFER += 1

    print('Errores: ' + str(ERROR_BUFFER) + '/' + str(TOTAL_BUFFER))
    time.sleep(TIME)
