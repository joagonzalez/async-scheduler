from flask_restx import Api, Resource
from settings import *

def create_restx_app():
    api = Api(version=CONFIG['RESTX']['VERSION'], title=CONFIG['RESTX']['TITLE'],
          description=CONFIG['RESTX']['DESCRIPTION'])
    return api
