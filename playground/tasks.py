from celery import shared_task
from time import sleep

@shared_task
def fun():
    print("Sending 10k emails...")
    sleep(10)
    print("Sent.")