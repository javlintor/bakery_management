from django.core.management.base import BaseCommand
from itertools import product
from typing import Optional, List
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from pydantic import PositiveInt
import datetime

from core.models import WeeklyDefaults, Order, Customer, Bread


class CustomerQueryError(Exception):
    pass


class InvalidDaysException(Exception):
    pass


def validate_days(days: int):
    if isinstance(days, int) and days >= 0:
        return
    else:
        raise InvalidDaysException


def get_customer_list(
        name: Optional[str] = None,
        lastname: Optional[str] = None
) -> List[Customer]:
    if name is None:
        customers = Customer.objects.all()
        return customers
    if lastname is None:
        raise CustomerQueryError("If name is not None, lastname must be not None")
    customer = get_customer(name, lastname)
    return [customer]


def get_customer(name: str, lastname: str) -> Customer:
    try:
        customer = Customer.objects.get(name=name, lastname=lastname)
        return customer
    except (MultipleObjectsReturned, ObjectDoesNotExist) as e:
        msg = f"""
        Error quering customer 
        name={name}, lastname={lastname}
        {e}
        """
        raise CustomerQueryError(msg)


class Command(BaseCommand):
    help = "Compute default orders based on weekly defaults"

    def add_arguments(self, parser):
        parser.add_argument(
            "--customer-name",
            help="Name of the customer whose defualt order is going to be computed. "
                 "If None, all customers will be computed"
        )
        parser.add_argument(
            "--customer-lastname",
            help="Lastname of the customer whose defualt order is going to be computed. "
                 "If --customer-name is None, this argument is ignored."
                 "If --customer-name is not None and --customer-lastname is, raise an exception"
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
            default=3,
            help="Number of days ahead for computation"
        )
        parser.add_argument(
            "--date-from",
            default=datetime.date.today(),
            type=lambda s: datetime.date.fromisoformat(s),
            help="First date for computation in YYYY-MM-DD format"
        )

    def handle(self, *args, **options):
        customer_name = options["customer_name"]
        customer_lastname = options["customer_lastname"]
        customers = get_customer_list(customer_name, customer_lastname)
        breads = Bread.objects.all()
        # validate weekday
        days: PositiveInt = options["days"]
        validate_days(days)
        # date_from
        date_from = options["date_from"]
        iterable = product(customers, breads, range(days))
        for customer, bread, days_future in iterable:
            date = date_from + datetime.timedelta(days=days_future)
            weekday = date.weekday()
            try:
                weekly_default = WeeklyDefaults.objects.get(
                    customer=customer, bread=bread, weekday=weekday
                )
            except WeeklyDefaults.DoesNotExist:
                continue
            order, created = Order.objects.get_or_create(
                customer=customer,
                bread=bread,
                date=date,
            )
            order.number = weekly_default.number
            order.save()
