import datetime
import pandas as pd
from typing import List, Dict
from django.shortcuts import render
from .models import Order
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def get_order_table(orders: List[Order]) -> pd.DataFrame:
    order_table = {}
    for order in orders:
        bread_key = order.bread.name
        customer_key = " ".join([order.customer.name, order.customer.lastname])
        try:
            order_table[customer_key][bread_key] = order.number
        except KeyError:
            order_table[customer_key] = {}
            order_table[customer_key][bread_key] = order.number

    order_table = pd.DataFrame(order_table)
    order_table = order_table.fillna(0)
    order_table = order_table.astype("int")
    return order_table


def index(request):
    date_str = request.GET.get('date')
    if date_str is None:
        print("parameter not found")
        date = datetime.date.today()
    else:
        print(f"got date: {date_str}")
        try:
            date = datetime.date.fromisoformat(date_str)
        except ValueError:
            print("Incorrent date format.")
            date = datetime.date.today()
    date_long_str = date.strftime('%A, %d de %B de %Y')
    orders = Order.objects.filter(date=date, number__gt=0)
    day_before = date - datetime.timedelta(days=1)
    day_before_iso = day_before.isoformat()
    day_after = date + datetime.timedelta(days=1)
    day_after_iso = day_after.isoformat()
    order_table = get_order_table(orders)
    order_table_html = order_table.to_html()
    context = {
        "today_str": date_long_str,
        "order_table": order_table,
        "day_before_iso": day_before_iso,
        "day_after_iso": day_after_iso
    }
    return render(request, "core/index.html", context)
