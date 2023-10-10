from django.core.management.base import BaseCommand
import random
from itertools import product

from core.models import Customer, Bread, WeeklyDefaults


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        # get customers
        customers = Customer.objects.all()
        # get breads
        breads = Bread.objects.all()
        # for earch weekday, create some defaults
        weekdays = [
            "lunes",
            "martes",
            "miércoles",
            "jueves",
            "viernes",
            "sábado",
            "domingo"
        ]
        for customer, bread, weekday in product(customers, breads, weekdays):
            number = random.randrange(5)
            weeklydefault = WeeklyDefaults(
                customer=customer,
                bread=bread,
                weekday=weekday,
                number=number
            )
            weeklydefault.save()
