from celery import shared_task
from time import sleep

@shared_task
def fun():
    print("Sending 10k emails...")
    sleep(10)
    print("Sent.")

@shared_task
def notify_customer(*args, **kwargs):
    print("notifying customer...", args)
    sleep(3)
    print("Sent.")