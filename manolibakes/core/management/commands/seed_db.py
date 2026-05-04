from datetime import UTC, datetime

from django.core.management.base import BaseCommand

from core.models import Bread, Customer, DailyDefaults, Order

BREAD_NAMES = ["baguette", "chapata", "molde", "centeno", "brioche"]

CUSTOMERS = [
    {"name": "Ana", "lastname": "García"},
    {"name": "Carlos", "lastname": "López"},
    {"name": "María", "lastname": "Martínez"},
    {"name": "Pedro", "lastname": "Sánchez"},
]

DAILY_DEFAULTS = [
    {"customer_index": 0, "bread_index": 0, "number": 3},
    {"customer_index": 0, "bread_index": 1, "number": 1},
    {"customer_index": 1, "bread_index": 0, "number": 5},
    {"customer_index": 1, "bread_index": 2, "number": 2},
    {"customer_index": 2, "bread_index": 3, "number": 4},
    {"customer_index": 3, "bread_index": 4, "number": 2},
    {"customer_index": 3, "bread_index": 0, "number": 6},
]

ORDER_OVERRIDES = [
    {"customer_index": 0, "bread_index": 0, "number": 10},
    {"customer_index": 1, "bread_index": 0, "number": 0},
    {"customer_index": 2, "bread_index": 3, "number": 7},
]


def create_breads() -> list[Bread]:
    breads = []
    for bread_name in BREAD_NAMES:
        bread, _ = Bread.objects.get_or_create(name=bread_name)
        breads.append(bread)
    return breads


def create_customers() -> list[Customer]:
    customers = []
    for customer_data in CUSTOMERS:
        customer, _ = Customer.objects.get_or_create(
            name=customer_data["name"],
            lastname=customer_data["lastname"],
        )
        customers.append(customer)
    return customers


def create_daily_defaults(customers: list[Customer], breads: list[Bread]) -> None:
    for default_data in DAILY_DEFAULTS:
        customer = customers[default_data["customer_index"]]
        bread = breads[default_data["bread_index"]]
        DailyDefaults.objects.get_or_create(
            customer=customer,
            bread=bread,
            defaults={"number": default_data["number"]},
        )


def create_order_overrides(customers: list[Customer], breads: list[Bread]) -> None:
    today = datetime.now(tz=UTC).date()
    for order_data in ORDER_OVERRIDES:
        customer = customers[order_data["customer_index"]]
        bread = breads[order_data["bread_index"]]
        Order.objects.get_or_create(
            customer=customer,
            bread=bread,
            date=today,
            defaults={"number": order_data["number"]},
        )


class Command(BaseCommand):
    help = "Seed the database with initial data for development"

    def handle(self, *args: object, **options: object) -> None:
        self.stdout.write("Creating breads...")
        breads = create_breads()

        self.stdout.write("Creating customers...")
        customers = create_customers()

        self.stdout.write("Creating daily defaults...")
        create_daily_defaults(customers=customers, breads=breads)

        self.stdout.write("Creating order overrides...")
        create_order_overrides(customers=customers, breads=breads)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
