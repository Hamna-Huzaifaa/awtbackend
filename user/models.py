import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add the related_name argument to the ManyToManyField fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='group_user',  # Provide a unique related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='permission_user',  # Provide a unique related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    # Your additional custom fields and methods

    class Meta:
        verbose_name_plural = 'users'

def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(4))
    if Requests.objects.filter(rid=key).exists():
        key = key_generator()
    return key

class Requests(models.Model):
    rid = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
