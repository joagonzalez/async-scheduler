### Celery using rabbitMQ as broker

Using producer-consumer approach allows to decouple task scheduling from workers that actually execute the task. This also allows to run code in workers regardless of their OS and having load balacing for task execution.


![Figura 1](https://github.com/joagonzalez/celery_poc/blob/master/doc/tasks_flow.png)

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

`/buffer/`
```
jgonzalez@godel:~$ curl http://127.0.0.1:5000/buffer | python -mjson.tool
{
    "result": "{'b9810946-ee45-4bd6-bae2-7eedea36d54e': <AsyncResult: b9810946-ee45-4bd6-bae2-7eedea36d54e>, '303a2d28-66ac-471f-bb61-6653d3950b58': <AsyncResult: 303a2d28-66ac-471f-bb61-6653d3950b58>, '654fcfa0-cc9a-4110-bb3b-13e5d6aae882': <AsyncResult: 654fcfa0-cc9a-4110-bb3b-13e5d6aae882>, 'faf161ae-b9b8-48fe-97c6-2251419ab896': <AsyncResult: faf161ae-b9b8-48fe-97c6-2251419ab896>, 'a24f9ed7-966f-46f8-943d-630fe2c40f3f': <AsyncResult: a24f9ed7-966f-46f8-943d-630fe2c40f3f>, 'bd9832de-c3ec-4738-b0c5-6d514249bf4a': <AsyncResult: bd9832de-c3ec-4738-b0c5-6d514249bf4a>, '4733d56e-1c91-4f1b-a72a-1901ce6e8e15': <AsyncResult: 4733d56e-1c91-4f1b-a72a-1901ce6e8e15>}"
}
```

#### Configure rabbitMQ
Port 8080 will expose RabbitMQ monitoring GUI
```
docker run -d --hostname rabbitmq-poc --name rabbitmq-poc -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```

#### Configure flower
Flower allows monitor Celery worker and also expose an API to manage the cluster
```
docker run -d --hostname flower-poc --name flower-poc -p 5555:5555 -p 8888:8888 mher/flower "flower --broker=pyamqp://guest@localhost// --port=8888" 

celery -A app.celery flower --port=5555 --address=0.0.0.0 --basic_auth=admin:admin --broker=pyamqp://guest@localhost// --broker_api=http://guest@localhost.com:8080/api
```

![Figura 2](https://github.com/joagonzalez/celery_poc/blob/master/doc/workers.png)

![Figura 3](https://github.com/joagonzalez/celery_poc/blob/master/doc/tasks.png)

![Figura 4](https://github.com/joagonzalez/celery_poc/blob/master/doc/time.png)
