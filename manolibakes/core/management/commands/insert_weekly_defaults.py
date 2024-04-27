from django.core.management.base import BaseCommand
import random
from itertools import product

from core.models import Customer, Bread, WeeklyDefaults


class Command(BaseCommand):

    def handle(self, *args, **options):
        # get customers
        customer = Customer.objects.get(pk=9)
        # get breads
        breads = Bread.objects.all()
        breads = breads[:3]
        for bread, weekday in product(
            breads, WeeklyDefaults.Weekday.values
        ):
            number = random.randrange(1, 5)
            weeklydefault = WeeklyDefaults(
                customer=customer, bread=bread, weekday=weekday, number=number
            )
            weeklydefault.save()
