from django.db import connection
from core.utils import get_post_data
from typing import Iterable
from core.models import DailyDefaults, Order
from core.dto import OrderDTO
from django.core.exceptions import ObjectDoesNotExist


def get_customer_final_orders(customer_id: int, date: str) -> list[OrderDTO]:
    query = """
        SELECT
            b.name,
            b.id,
            COALESCE(COALESCE(o.number, dd.number), 0) AS number
        FROM core_bread b
        LEFT OUTER JOIN core_dailydefaults dd
        ON dd.bread_id = b.id AND dd.customer_id = %s
        LEFT OUTER JOIN core_order o
        ON o.bread_id = b.id AND o.customer_id = %s AND o.date = %s
        ORDER BY number DESC, name;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [customer_id, customer_id, date])
        orders = cursor.fetchall()
    orders = [OrderDTO(name=order[0], id=order[1], number=order[2]) for order in orders]
    return orders


def save_customer_daily_defaults(request, customer_id):
    data = get_post_data(request)
    for bread_id, number in data:
        number = int(number)
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


def get_daily_defaults(customer_id) -> Iterable[OrderDTO]:
    query = """
        SELECT b.name, b.id, COALESCE(dd.number, 0) AS number FROM core_bread b
        LEFT OUTER JOIN core_dailydefaults dd
        ON dd.bread_id = b.id AND dd.customer_id = %s
        ORDER BY number DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [customer_id])
        daily_defaults = cursor.fetchall()
    daily_defaults = [
        OrderDTO(name=daily_default[0], id=daily_default[1], number=daily_default[2])
        for daily_default in daily_defaults
    ]
    return daily_defaults


def save_customer_data(request, customer_id, date):
    data = get_post_data(request)
    for bread_id, number in data:
        number = int(number)
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
