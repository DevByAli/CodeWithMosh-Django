from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer


# After creating the signal it should be register in app.
# In `app.py` we import it.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_on_new_user(sender, **kwargs):
    if kwargs.get('created'):
        Customer.objects.create(user=kwargs['instance'])