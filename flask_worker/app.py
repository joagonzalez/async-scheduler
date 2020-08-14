from flask import Flask
import logging
from app_library import setup_logging, CONFIG
from bootstrap import create_app

# configure logger
setup_logging(default_path='logging.json')
logger = logging.getLogger(CONFIG['FLASK']['LOGGER']) # use logger instead of logging
# logger.info("hola")
# logger.error("chau")
# logger.debug("pepitor")

# congure flask app
app_flask = Flask(__name__)

if __name__ == '__main__':
    create_app(app_flask, logger)