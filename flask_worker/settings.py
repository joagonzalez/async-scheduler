CONFIG = {
            'CELERY': {
                'CELERY_BROKER_URL': 'pyamqp://guest@localhost//',
                'CELERY_BACKEND': 'rpc://',
                'ACCEPT_CONTENT':  ['pickle', 'json', 'x-python-serialize', 'application/x-python-serialize'],
                'TASK_SERIALIZER': 'pickle'
            },
            'FLASK' : {
                'DEBUG': True,
                'HOSTNAME': 'newcos-sandbox-04.smq.net',
                'PORT': 5000,
                'LOGGER': 'app_production'
            },
            'RESTX': {
                'VERSION': '1.0',
                'TITLE': 'Powershell Helper API',
                'DESCRIPTION': 'Flask restx API that works with celery workers to execute general purpose scripts.'
            },
            'TEAMS': {
                'WEBHOOK_URL': 'https://outlook.office.com/webhook/327044bc-8860-4705-a521-48cc9bfd264e@58005ddb-3d82-4718-9e75-ec5c71cca7ec/IncomingWebhook/ce255d45adfd4d94aa803a84e86e1d6f/4b94f775-45ba-4f8d-a767-252cb12f9726'

            }
        }


