from django.dispatch import receiver
from store.signals import sig_order_created
from store.models import Order


@receiver(sig_order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])