from django.contrib import admin
from .models import Customer, Bread, Order, DailyDefaults

# Register your models here.
admin.site.register([Customer, Bread, DailyDefaults, Order])
