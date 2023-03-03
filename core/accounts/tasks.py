from celery import shared_task
from time import sleep
from core.celery import app
from celery.result import states, AsyncResult

@shared_task
def sendTest():
    sleep(3)
    print("Test sent")


