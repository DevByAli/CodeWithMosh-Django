import json
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

"""
1. python manage.py notify_customer
2. celery -A storefront beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
3. celery -A storefront worker --loglevel=info
"""
class Command(BaseCommand):

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.SECONDS,
        )

        if not created:
            self.stdout.write("Task already created")

        periodic_task, created = PeriodicTask.objects.update_or_create(
            {
                "name": 'Notify Customers'
            },
            {
                "interval": schedule,                  # we created this above.
                "name": 'Notify Customers',          # simply describes this periodic task.
                "task":'playground.tasks.notify_customer',  # name of task.
                "args":json.dumps(["New tasks"]),
            }
        )

        if not created:
            self.stdout.write("Task Update")
            