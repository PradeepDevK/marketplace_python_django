from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrator', 'ADMINISTRATOR'),
        ('hr', 'HR'),
        ('staff', 'STAFF'),
    )
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change 'custom_user_set' to something unique if needed
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change 'custom_user_permissions_set' to something unique if needed
        blank=True
    )