from django.core.management.base import BaseCommand
import random
from itertools import product

from core.models import Customer, Bread, WeeklyDefaults


class Command(BaseCommand):

    def handle(self, *args, **options):
        # get customers
        customers = Customer.objects.all()
        # get breads
        breads = Bread.objects.all()
        for customer, bread, weekday in product(customers, breads, WeeklyDefaults.Weekday.values):
            number = random.randrange(5)
            weeklydefault = WeeklyDefaults(
                customer=customer,
                bread=bread,
                weekday=weekday,
                number=number
            )
            weeklydefault.save()
