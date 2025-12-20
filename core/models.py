from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
"""
It is always recommended either you want to change the Authentication flow or not.
Always make the Custom User model like this. Because in future it will allow to swap 
the user with new user in middle of the project.

If you want to swap in middle of project the only solution is to drop DB and create New one.
"""

class User(AbstractUser):
    first_name = models.CharField(null=False, max_length=150)
    last_name = models.CharField(null=False, max_length=150)
    email = models.EmailField(unique=True)