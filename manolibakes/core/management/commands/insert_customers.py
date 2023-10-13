from django.core.management.base import BaseCommand

from core.models import Customer


class Command(BaseCommand):
    help = "Create and insert sample customers"

    def handle(self, *args, **options):
        new_customers = [
            Customer(name="Javier", lastname="Olarte"),
            Customer(name="Javier", lastname="Linares"),
            Customer(name="Domingo", lastname="Palomar"),
            Customer(name="Claudia", lastname="Palomar"),
            Customer(name="Marina", lastname="Palomar Ávila"),
        ]
        for customer in new_customers:
            customer.save()
