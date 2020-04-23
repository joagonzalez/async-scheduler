### Celery using rabbitMQ as broker

**Celery + two workers**
Run celery workers
```
cd single_worker

celery -A tasks worker --loglevel=info -n worker1
celery -A tasks worker --loglevel=info -n worker2
```

**Celery + flask**
```
cd flask_worker

python3 app.py
celery -A app.celery worker --loglevel=info -n worker1
celery -A app.celery worker --loglevel=info -n worker2
```


`/process/<word>`
```
jgonzalez@godel:~$ curl http://127.0.0.1:5000/process/joaquin | python -mjson.tool

{
    "buffer_status": "{ '5a636196-ba86-4e58-a770-9ae46df2199c': <AsyncResult: a19712ea-ac8a-4523-89d6-09c89b753250>}",
    "name": "joaquin",
    "scheduled": true,
    "status": "will be ready in 10 sec",
    "task_state": "PENDING",
    "taskid": "5a636196-ba86-4e58-a770-9ae46df2199c"
}
```

`/status/<taskid>`
```

jgonzalez@godel:~$ curl http://127.0.0.1:5000/status/5a636196-ba86-4e58-a770-9ae46df2199c |  python -mjson.tool

{
    "result": "Not ready",
    "status": "PENDING"
}

jgonzalez@godel:~$ curl http://127.0.0.1:5000/status/5a636196-ba86-4e58-a770-9ae46df2199c |  python -mjson.tool

{
    "result": "niuqaoj",
    "status": "SUCCESS"
}

```

#### Configure rabbitMQ

```
docker run -d -p 5672:5672 rabbitmq
```