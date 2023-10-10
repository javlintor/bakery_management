from django.core.management.base import BaseCommand

from core.models import WeeklyDefaults


class Command(BaseCommand):
    help = "Compute default orders based on weekly defaults"

    def add_arguments(self, parser):
        parser.add_argument(
            "--customer-name",
            help="Name of the customer whose defualt order is going to be computed. "
            "If None, all customers will be computed"
        )
        parser.add_argument(
            "--weekday",
            help="Name of the weekday whose defualt order is going to be computed. "
            "If None, all weekdays will be computed"
        )
        parser.add_argument(
            "--bread",
            help="Name of the bread whose defualt order is going to be computed. "
            "If None, all breads will be computed"
        )
        parser.add_argument(
            "--days",
            default=30,
            help="Number of days ahead for computation"
        )

    def handle(self, *args, **options):
        print(options["customer_name"])
        print(type(options["customer_name"]))

