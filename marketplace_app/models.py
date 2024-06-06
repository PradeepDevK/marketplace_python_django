from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User
from django.conf import settings

"""
Models for Categories
"""
class Category(models.Model):
    name  = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    
"""
Models for Products
"""
class Product(models.Model):
    product_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productlist')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = ArrayField(models.CharField(max_length=255), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title