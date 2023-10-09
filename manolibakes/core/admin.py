from django.contrib import admin
from .models import Customer, Bread, WeeklyDefaults, Order

# Register your models here.
admin.site.register([Customer, Bread, WeeklyDefaults, Order])
