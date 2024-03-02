from django.contrib import admin
from .models import Customer, Bread, WeeklyDefaults, Order, DailyDefaults

# Register your models here.
admin.site.register([Customer, Bread, WeeklyDefaults, DailyDefaults, Order])
