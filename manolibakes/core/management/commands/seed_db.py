from datetime import UTC, datetime, timedelta

from django.core.management.base import BaseCommand

from core.models import Bread, Customer, DailyDefaults, Order

BREAD_NAMES = ["baguette", "chapata", "molde", "centeno", "brioche"]

CUSTOMERS = [
    # Indices 0-4: no daily defaults
    {"name": "Ana", "lastname": "García"},
    {"name": "Carlos", "lastname": "López"},
    {"name": "María", "lastname": "Martínez"},
    {"name": "Pedro", "lastname": "Sánchez"},
    {"name": "Lucía", "lastname": "Pérez"},
    # Indices 5-9: defaults for all 5 breads
    {"name": "Javier", "lastname": "González"},
    {"name": "Carmen", "lastname": "Rodríguez"},
    {"name": "Antonio", "lastname": "Fernández"},
    {"name": "Isabel", "lastname": "Hernández"},
    {"name": "Manuel", "lastname": "Jiménez"},
    # Indices 10-49: defaults for 2-3 breads
    {"name": "Elena", "lastname": "Ruiz"},
    {"name": "Francisco", "lastname": "Díaz"},
    {"name": "Sofía", "lastname": "Moreno"},
    {"name": "José", "lastname": "Álvarez"},
    {"name": "Laura", "lastname": "Romero"},
    {"name": "Miguel", "lastname": "Alonso"},
    {"name": "Paula", "lastname": "Gutiérrez"},
    {"name": "David", "lastname": "Navarro"},
    {"name": "Andrea", "lastname": "Torres"},
    {"name": "Daniel", "lastname": "Domínguez"},
    {"name": "Marta", "lastname": "Vázquez"},
    {"name": "Alejandro", "lastname": "Ramos"},
    {"name": "Cristina", "lastname": "Gil"},
    {"name": "Pablo", "lastname": "Ramírez"},
    {"name": "Beatriz", "lastname": "Serrano"},
    {"name": "Sergio", "lastname": "Blanco"},
    {"name": "Patricia", "lastname": "Molina"},
    {"name": "Adrián", "lastname": "Morales"},
    {"name": "Raquel", "lastname": "Suárez"},
    {"name": "Diego", "lastname": "Ortega"},
    {"name": "Natalia", "lastname": "Delgado"},
    {"name": "Álvaro", "lastname": "Castro"},
    {"name": "Silvia", "lastname": "Ortiz"},
    {"name": "Iván", "lastname": "Rubio"},
    {"name": "Eva", "lastname": "Marín"},
    {"name": "Rubén", "lastname": "Sanz"},
    {"name": "Rocío", "lastname": "Iglesias"},
    {"name": "Jorge", "lastname": "Medina"},
    {"name": "Mónica", "lastname": "Garrido"},
    {"name": "Óscar", "lastname": "Cortés"},
    {"name": "Pilar", "lastname": "Castillo"},
    {"name": "Ignacio", "lastname": "Santos"},
    {"name": "Teresa", "lastname": "Lozano"},
    {"name": "Roberto", "lastname": "Guerrero"},
    {"name": "Susana", "lastname": "Cano"},
    {"name": "Fernando", "lastname": "Prieto"},
    {"name": "Inés", "lastname": "Méndez"},
    {"name": "Gonzalo", "lastname": "Cruz"},
    {"name": "Alicia", "lastname": "Calvo"},
    {"name": "Ricardo", "lastname": "Gallego"},
]

DAILY_DEFAULTS = [
    # Customers 5-9: all 5 breads
    {"customer_index": 5, "bread_index": 0, "number": 3},
    {"customer_index": 5, "bread_index": 1, "number": 2},
    {"customer_index": 5, "bread_index": 2, "number": 1},
    {"customer_index": 5, "bread_index": 3, "number": 4},
    {"customer_index": 5, "bread_index": 4, "number": 2},
    {"customer_index": 6, "bread_index": 0, "number": 5},
    {"customer_index": 6, "bread_index": 1, "number": 3},
    {"customer_index": 6, "bread_index": 2, "number": 2},
    {"customer_index": 6, "bread_index": 3, "number": 1},
    {"customer_index": 6, "bread_index": 4, "number": 4},
    {"customer_index": 7, "bread_index": 0, "number": 2},
    {"customer_index": 7, "bread_index": 1, "number": 4},
    {"customer_index": 7, "bread_index": 2, "number": 3},
    {"customer_index": 7, "bread_index": 3, "number": 2},
    {"customer_index": 7, "bread_index": 4, "number": 1},
    {"customer_index": 8, "bread_index": 0, "number": 1},
    {"customer_index": 8, "bread_index": 1, "number": 2},
    {"customer_index": 8, "bread_index": 2, "number": 3},
    {"customer_index": 8, "bread_index": 3, "number": 4},
    {"customer_index": 8, "bread_index": 4, "number": 5},
    {"customer_index": 9, "bread_index": 0, "number": 6},
    {"customer_index": 9, "bread_index": 1, "number": 1},
    {"customer_index": 9, "bread_index": 2, "number": 2},
    {"customer_index": 9, "bread_index": 3, "number": 1},
    {"customer_index": 9, "bread_index": 4, "number": 3},
    # Customers 10-49: 2-3 breads each
    {"customer_index": 10, "bread_index": 0, "number": 3},
    {"customer_index": 10, "bread_index": 2, "number": 1},
    {"customer_index": 11, "bread_index": 1, "number": 2},
    {"customer_index": 11, "bread_index": 3, "number": 4},
    {"customer_index": 11, "bread_index": 4, "number": 1},
    {"customer_index": 12, "bread_index": 0, "number": 5},
    {"customer_index": 12, "bread_index": 1, "number": 2},
    {"customer_index": 13, "bread_index": 2, "number": 3},
    {"customer_index": 13, "bread_index": 4, "number": 1},
    {"customer_index": 14, "bread_index": 0, "number": 4},
    {"customer_index": 14, "bread_index": 3, "number": 2},
    {"customer_index": 14, "bread_index": 4, "number": 1},
    {"customer_index": 15, "bread_index": 1, "number": 3},
    {"customer_index": 15, "bread_index": 2, "number": 2},
    {"customer_index": 16, "bread_index": 0, "number": 6},
    {"customer_index": 16, "bread_index": 4, "number": 2},
    {"customer_index": 17, "bread_index": 1, "number": 1},
    {"customer_index": 17, "bread_index": 2, "number": 3},
    {"customer_index": 17, "bread_index": 3, "number": 2},
    {"customer_index": 18, "bread_index": 3, "number": 4},
    {"customer_index": 18, "bread_index": 4, "number": 1},
    {"customer_index": 19, "bread_index": 0, "number": 2},
    {"customer_index": 19, "bread_index": 1, "number": 3},
    {"customer_index": 19, "bread_index": 4, "number": 1},
    {"customer_index": 20, "bread_index": 2, "number": 4},
    {"customer_index": 20, "bread_index": 3, "number": 2},
    {"customer_index": 21, "bread_index": 0, "number": 1},
    {"customer_index": 21, "bread_index": 1, "number": 2},
    {"customer_index": 21, "bread_index": 2, "number": 3},
    {"customer_index": 22, "bread_index": 1, "number": 5},
    {"customer_index": 22, "bread_index": 4, "number": 2},
    {"customer_index": 23, "bread_index": 0, "number": 3},
    {"customer_index": 23, "bread_index": 3, "number": 1},
    {"customer_index": 24, "bread_index": 2, "number": 2},
    {"customer_index": 24, "bread_index": 3, "number": 4},
    {"customer_index": 24, "bread_index": 4, "number": 1},
    {"customer_index": 25, "bread_index": 0, "number": 4},
    {"customer_index": 25, "bread_index": 2, "number": 2},
    {"customer_index": 26, "bread_index": 1, "number": 3},
    {"customer_index": 26, "bread_index": 3, "number": 2},
    {"customer_index": 27, "bread_index": 0, "number": 5},
    {"customer_index": 27, "bread_index": 1, "number": 1},
    {"customer_index": 27, "bread_index": 4, "number": 3},
    {"customer_index": 28, "bread_index": 2, "number": 1},
    {"customer_index": 28, "bread_index": 4, "number": 4},
    {"customer_index": 29, "bread_index": 0, "number": 2},
    {"customer_index": 29, "bread_index": 1, "number": 3},
    {"customer_index": 29, "bread_index": 3, "number": 1},
    {"customer_index": 30, "bread_index": 3, "number": 2},
    {"customer_index": 30, "bread_index": 4, "number": 5},
    {"customer_index": 31, "bread_index": 0, "number": 3},
    {"customer_index": 31, "bread_index": 2, "number": 1},
    {"customer_index": 31, "bread_index": 4, "number": 2},
    {"customer_index": 32, "bread_index": 1, "number": 4},
    {"customer_index": 32, "bread_index": 3, "number": 2},
    {"customer_index": 33, "bread_index": 0, "number": 6},
    {"customer_index": 33, "bread_index": 4, "number": 1},
    {"customer_index": 34, "bread_index": 1, "number": 2},
    {"customer_index": 34, "bread_index": 2, "number": 3},
    {"customer_index": 34, "bread_index": 4, "number": 1},
    {"customer_index": 35, "bread_index": 2, "number": 4},
    {"customer_index": 35, "bread_index": 3, "number": 2},
    {"customer_index": 36, "bread_index": 0, "number": 3},
    {"customer_index": 36, "bread_index": 1, "number": 1},
    {"customer_index": 37, "bread_index": 2, "number": 2},
    {"customer_index": 37, "bread_index": 4, "number": 3},
    {"customer_index": 38, "bread_index": 0, "number": 4},
    {"customer_index": 38, "bread_index": 1, "number": 2},
    {"customer_index": 38, "bread_index": 3, "number": 1},
    {"customer_index": 39, "bread_index": 1, "number": 5},
    {"customer_index": 39, "bread_index": 4, "number": 1},
    {"customer_index": 40, "bread_index": 0, "number": 2},
    {"customer_index": 40, "bread_index": 2, "number": 3},
    {"customer_index": 40, "bread_index": 3, "number": 1},
    {"customer_index": 41, "bread_index": 3, "number": 4},
    {"customer_index": 41, "bread_index": 4, "number": 2},
    {"customer_index": 42, "bread_index": 0, "number": 5},
    {"customer_index": 42, "bread_index": 2, "number": 1},
    {"customer_index": 43, "bread_index": 1, "number": 2},
    {"customer_index": 43, "bread_index": 2, "number": 1},
    {"customer_index": 43, "bread_index": 3, "number": 3},
    {"customer_index": 44, "bread_index": 0, "number": 3},
    {"customer_index": 44, "bread_index": 4, "number": 2},
    {"customer_index": 45, "bread_index": 1, "number": 1},
    {"customer_index": 45, "bread_index": 3, "number": 4},
    {"customer_index": 46, "bread_index": 0, "number": 2},
    {"customer_index": 46, "bread_index": 1, "number": 3},
    {"customer_index": 46, "bread_index": 2, "number": 1},
    {"customer_index": 47, "bread_index": 3, "number": 5},
    {"customer_index": 47, "bread_index": 4, "number": 2},
    {"customer_index": 48, "bread_index": 0, "number": 1},
    {"customer_index": 48, "bread_index": 2, "number": 4},
    {"customer_index": 48, "bread_index": 4, "number": 2},
    {"customer_index": 49, "bread_index": 1, "number": 3},
    {"customer_index": 49, "bread_index": 2, "number": 1},
]

ORDER_OVERRIDES = [
    # Past week (day_offset -7 to -1)
    {"customer_index": 0, "bread_index": 0, "number": 4, "day_offset": -7},
    {"customer_index": 5, "bread_index": 0, "number": 6, "day_offset": -7},
    {"customer_index": 12, "bread_index": 1, "number": 0, "day_offset": -6},
    {"customer_index": 18, "bread_index": 3, "number": 8, "day_offset": -6},
    {"customer_index": 1, "bread_index": 2, "number": 3, "day_offset": -5},
    {"customer_index": 7, "bread_index": 4, "number": 0, "day_offset": -5},
    {"customer_index": 22, "bread_index": 1, "number": 7, "day_offset": -5},
    {"customer_index": 9, "bread_index": 0, "number": 10, "day_offset": -4},
    {"customer_index": 30, "bread_index": 4, "number": 0, "day_offset": -4},
    {"customer_index": 2, "bread_index": 1, "number": 5, "day_offset": -3},
    {"customer_index": 14, "bread_index": 0, "number": 0, "day_offset": -3},
    {"customer_index": 25, "bread_index": 2, "number": 6, "day_offset": -3},
    {"customer_index": 6, "bread_index": 4, "number": 8, "day_offset": -2},
    {"customer_index": 33, "bread_index": 0, "number": 0, "day_offset": -2},
    {"customer_index": 41, "bread_index": 3, "number": 6, "day_offset": -2},
    {"customer_index": 3, "bread_index": 0, "number": 4, "day_offset": -1},
    {"customer_index": 17, "bread_index": 2, "number": 0, "day_offset": -1},
    {"customer_index": 38, "bread_index": 1, "number": 5, "day_offset": -1},
    # Today
    {"customer_index": 0, "bread_index": 0, "number": 10, "day_offset": 0},
    {"customer_index": 1, "bread_index": 0, "number": 0, "day_offset": 0},
    {"customer_index": 2, "bread_index": 3, "number": 7, "day_offset": 0},
    {"customer_index": 8, "bread_index": 2, "number": 0, "day_offset": 0},
    {"customer_index": 19, "bread_index": 4, "number": 5, "day_offset": 0},
    {"customer_index": 27, "bread_index": 0, "number": 9, "day_offset": 0},
    # Next week (day_offset 1-7)
    {"customer_index": 4, "bread_index": 1, "number": 3, "day_offset": 1},
    {"customer_index": 11, "bread_index": 3, "number": 0, "day_offset": 1},
    {"customer_index": 5, "bread_index": 2, "number": 4, "day_offset": 2},
    {"customer_index": 21, "bread_index": 0, "number": 0, "day_offset": 2},
    {"customer_index": 35, "bread_index": 3, "number": 6, "day_offset": 2},
    {"customer_index": 13, "bread_index": 2, "number": 0, "day_offset": 3},
    {"customer_index": 28, "bread_index": 4, "number": 8, "day_offset": 3},
    {"customer_index": 6, "bread_index": 0, "number": 10, "day_offset": 4},
    {"customer_index": 44, "bread_index": 0, "number": 0, "day_offset": 4},
    {"customer_index": 16, "bread_index": 4, "number": 5, "day_offset": 5},
    {"customer_index": 29, "bread_index": 1, "number": 0, "day_offset": 5},
    {"customer_index": 7, "bread_index": 1, "number": 7, "day_offset": 6},
    {"customer_index": 40, "bread_index": 2, "number": 0, "day_offset": 6},
    {"customer_index": 9, "bread_index": 3, "number": 4, "day_offset": 7},
    {"customer_index": 24, "bread_index": 4, "number": 0, "day_offset": 7},
    # Two-week mark (day_offset 8-14)
    {"customer_index": 10, "bread_index": 0, "number": 6, "day_offset": 8},
    {"customer_index": 36, "bread_index": 1, "number": 0, "day_offset": 9},
    {"customer_index": 5, "bread_index": 1, "number": 5, "day_offset": 10},
    {"customer_index": 23, "bread_index": 3, "number": 0, "day_offset": 10},
    {"customer_index": 47, "bread_index": 4, "number": 7, "day_offset": 10},
    {"customer_index": 12, "bread_index": 0, "number": 8, "day_offset": 11},
    {"customer_index": 31, "bread_index": 2, "number": 0, "day_offset": 12},
    {"customer_index": 8, "bread_index": 4, "number": 9, "day_offset": 13},
    {"customer_index": 42, "bread_index": 0, "number": 0, "day_offset": 14},
    # Three to four weeks (day_offset 15-30)
    {"customer_index": 0, "bread_index": 2, "number": 5, "day_offset": 15},
    {"customer_index": 17, "bread_index": 1, "number": 0, "day_offset": 17},
    {"customer_index": 6, "bread_index": 2, "number": 6, "day_offset": 18},
    {"customer_index": 26, "bread_index": 1, "number": 0, "day_offset": 20},
    {"customer_index": 33, "bread_index": 4, "number": 4, "day_offset": 21},
    {"customer_index": 1, "bread_index": 3, "number": 6, "day_offset": 22},
    {"customer_index": 7, "bread_index": 2, "number": 0, "day_offset": 24},
    {"customer_index": 45, "bread_index": 3, "number": 5, "day_offset": 25},
    {"customer_index": 19, "bread_index": 0, "number": 0, "day_offset": 27},
    {"customer_index": 9, "bread_index": 4, "number": 7, "day_offset": 28},
    {"customer_index": 38, "bread_index": 0, "number": 0, "day_offset": 30},
    # Second month (day_offset 31-60)
    {"customer_index": 3, "bread_index": 1, "number": 4, "day_offset": 32},
    {"customer_index": 15, "bread_index": 2, "number": 0, "day_offset": 34},
    {"customer_index": 5, "bread_index": 4, "number": 8, "day_offset": 35},
    {"customer_index": 49, "bread_index": 1, "number": 0, "day_offset": 37},
    {"customer_index": 8, "bread_index": 3, "number": 6, "day_offset": 39},
    {"customer_index": 20, "bread_index": 2, "number": 0, "day_offset": 41},
    {"customer_index": 6, "bread_index": 1, "number": 5, "day_offset": 43},
    {"customer_index": 32, "bread_index": 1, "number": 0, "day_offset": 45},
    {"customer_index": 4, "bread_index": 0, "number": 7, "day_offset": 47},
    {"customer_index": 9, "bread_index": 2, "number": 0, "day_offset": 49},
    {"customer_index": 43, "bread_index": 2, "number": 4, "day_offset": 51},
    {"customer_index": 7, "bread_index": 3, "number": 0, "day_offset": 53},
    {"customer_index": 2, "bread_index": 4, "number": 6, "day_offset": 55},
    {"customer_index": 46, "bread_index": 0, "number": 0, "day_offset": 57},
    {"customer_index": 8, "bread_index": 0, "number": 9, "day_offset": 60},
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
        date = today + timedelta(days=order_data["day_offset"])
        Order.objects.get_or_create(
            customer=customer,
            bread=bread,
            date=date,
            defaults={"number": order_data["number"]},
        )


class Command(BaseCommand):
    help = "Seed the database with initial data for development"

    def handle(self, *args: object, **options: object) -> None:  # noqa: ARG002
        self.stdout.write("Creating breads...")
        breads = create_breads()

        self.stdout.write("Creating customers...")
        customers = create_customers()

        self.stdout.write("Creating daily defaults...")
        create_daily_defaults(customers=customers, breads=breads)

        self.stdout.write("Creating order overrides...")
        create_order_overrides(customers=customers, breads=breads)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))

