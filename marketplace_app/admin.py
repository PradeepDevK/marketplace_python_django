from django.contrib import admin
from marketplace_app.models import (
    Category,
    Product,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)