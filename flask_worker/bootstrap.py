from flask import Blueprint
from app_library import *
from services.restxService import create_restx_app
from api import ns as async_namespace
from celery import Celery

def config_flask_app(flask_app):
    flask_app.config['CELERY_BROKER_URL'] = CONFIG['CELERY']['CELERY_BROKER_URL']
    flask_app.config['CELERY_BACKEND'] = CONFIG['CELERY']['CELERY_BACKEND']
    flask_app.config['ACCEPT_CONTENT'] = CONFIG['CELERY']['ACCEPT_CONTENT']
    flask_app.config['TASK_SERIALIZER'] = CONFIG['CELERY']['TASK_SERIALIZER']
    flask_app.config['CELERY_CREATE_MISSING_QUEUES'] = CONFIG['CELERY']['CELERY_CREATE_MISSING_QUEUES']

    return flask_app

def register_service(logger):
    pass

# bootstrap flask app
def create_app(flask_app, logger):  

    register_service(logger)
    config_flask_app(flask_app)
    #init_celery(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/')  
    api = create_restx_app()
    api.init_app(blueprint)
    api.add_namespace(async_namespace)
    flask_app.register_blueprint(blueprint)

    flask_app.run(host=CONFIG['FLASK']['HOSTNAME'], port=CONFIG['FLASK']['PORT'], debug=CONFIG['FLASK']['DEBUG'])

