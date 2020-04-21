### Celery using rabbitMQ as broker

**Celery + two workers**
Run celery workers
```
celery -A tasks worker --loglevel=info -n worker1
celery -A tasks worker --loglevel=info -n worker2

```

**Celery + flask**


#### Configure rabbitMQ

```
docker run -d -p 5672:5672 rabbitmq
```