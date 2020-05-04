import os
import sys
import time
import json
import requests
import pymsteams
import logging, logging.config
from settings import *

# general purpose functions
def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def send_teams_message(message):
    myTeamsMessage = pymsteams.connectorcard(CONFIG['TEAMS']['WEBHOOK_URL'])
    myTeamsMessage.text(message)
    result = myTeamsMessage.send()
    return result

def register_service(logger):
    logger.debug('Register service....')
    # logger.info('Register service....')
    # logger.warning('Register service....')
    # logger.error('Register service....')

# bootstrap flask app
def create_app(app, logger):  
    register_service(logger)  
    app.run(host=CONFIG['FLASK']['HOSTNAME'], port=CONFIG['FLASK']['PORT'], debug=CONFIG['FLASK']['DEBUG'])
