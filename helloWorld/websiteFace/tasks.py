from celery import Celery
import time

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//', backend="rpc://")

@app.task
def a():
    time.sleep(10)
    return "!!!!!!!!!"
    