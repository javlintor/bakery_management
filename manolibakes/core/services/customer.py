from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import IntegerField, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from core.dto import OrderDTO
from core.models import Bread, DailyDefaults, Order
from core.utils import extract_bread_quantities

if TYPE_CHECKING:
    import datetime

    from django.http import HttpRequest


def get_customer_final_orders(customer_id: int, date: datetime.date) -> list[OrderDTO]:
    order_number_subquery = Subquery(
        Order.objects.filter(
            bread=OuterRef("pk"),
            customer_id=customer_id,
            date=date,
        ).values("number")[:1]
    )
    daily_default_number_subquery = Subquery(
        DailyDefaults.objects.filter(
            bread=OuterRef("pk"),
            customer_id=customer_id,
        ).values("number")[:1]
    )
    number_annotation = Coalesce(
        order_number_subquery,
        daily_default_number_subquery,
        Value(0),
        output_field=IntegerField(),
    )
    breads = Bread.objects.annotate(number=number_annotation).order_by(
        "-number", "name"
    )
    return [
        OrderDTO(name=bread.name, id=bread.id, number=bread.number) for bread in breads
    ]


def get_daily_defaults(customer_id: int) -> list[OrderDTO]:
    daily_default_number_subquery = Subquery(
        DailyDefaults.objects.filter(
            bread=OuterRef("pk"),
            customer_id=customer_id,
        ).values("number")[:1]
    )
    number_annotation = Coalesce(
        daily_default_number_subquery,
        Value(0),
        output_field=IntegerField(),
    )
    breads = Bread.objects.annotate(number=number_annotation).order_by("name")
    return [
        OrderDTO(name=bread.name, id=bread.id, number=bread.number) for bread in breads
    ]


@transaction.atomic
def save_customer_daily_defaults(request: HttpRequest, customer_id: int) -> None:
    data = extract_bread_quantities(post_data=request.POST)
    for bread_id, number in data:
        try:
            daily_default = DailyDefaults.objects.get(
                customer_id=customer_id, bread_id=bread_id
            )
            if number == 0:
                daily_default.delete()
                continue
            daily_default.number = number
        except ObjectDoesNotExist:
            if number == 0:
                continue
            daily_default = DailyDefaults(
                customer_id=customer_id, bread_id=bread_id, number=number
            )
        daily_default.save()


@transaction.atomic
def save_customer_data(
    request: HttpRequest, customer_id: int, date: str | None
) -> None:
    data = extract_bread_quantities(post_data=request.POST)
    for bread_id, number in data:
        order_exists = True
        try:
            order = Order.objects.get(
                customer_id=customer_id, bread_id=bread_id, date=date
            )
            order_number = order.number
        except ObjectDoesNotExist:
            order_exists = False
            order_number = 0
        try:
            daily_default = DailyDefaults.objects.get(
                customer_id=customer_id, bread_id=bread_id
            )
            daily_default_number = daily_default.number
        except ObjectDoesNotExist:
            daily_default_number = 0
        if number == order_number:
            continue

        if number == daily_default_number:
            if order_exists:
                order.delete()
            continue

        if order_exists:
            order.number = number
            order.save()
            continue

        new_order = Order(
            customer_id=customer_id, bread_id=bread_id, date=date, number=number
        )
        new_order.save()

