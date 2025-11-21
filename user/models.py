from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

"""
Can be used to extend current user app to accomadate more userspecifc features
"""


class User(AbstractUser):
    pass
