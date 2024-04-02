import datetime
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from .models import Order, Customer, Bread, DailyDefaults
from core.utils import get_post_data
import locale
import logging

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def get_dates(date_str):
    if date_str is None:
        date = datetime.date.today()
    else:
        try:
            date = datetime.date.fromisoformat(date_str)
        except ValueError:
            logging.info("Incorrent date format.")
            date = datetime.date.today()
    date_long_str = date.strftime("%A, %d de %B de %Y")
    day_before = date - datetime.timedelta(days=1)
    day_before_iso = day_before.isoformat()
    day_after = date + datetime.timedelta(days=1)
    day_after_iso = day_after.isoformat()
    return {
        "date": date,
        "day_before_iso": day_before_iso,
        "day_after_iso": day_after_iso,
        "date_long_str": date_long_str,
    }


def index(request, date=None):
    dates = get_dates(date)
    orders = Bread.objects.filter(order__date=dates["date"]).annotate(
        total_units=Sum("order__number")
    )
    context = {"orders": orders, **dates}
    return render(request, "core/index.html", context)


def customers(request, date=None):
    dates = get_dates(date)
    customers = Customer.objects.all().order_by("name", "lastname")
    context = {"customers": customers, **dates}
    return render(request, "core/customers.html", context)


def breads(request, date=None):
    dates = get_dates(date)
    breads = Bread.objects.all()
    context = {"breads": breads, **dates}
    return render(request, "core/breads.html", context)


def save_customer_data(request, customer_id, date):
    data = get_post_data(request)
    for bread_id, number in data:
        order = Order.objects.get(customer_id=customer_id, date=date, bread_id=bread_id)
        order.number = int(number)
        order.save()


def save_customer_daily_defaults(request, customer_id):
    data = get_post_data(request)
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


def customer(request, customer_id, date):
    if request.method == "POST":
        save_customer_data(request, customer_id, date)
        return HttpResponseRedirect(reverse("core:index"))
    dates = get_dates(date)
    orders = Order.objects.filter(customer_id=customer_id, date=dates["date"])
    customer = Customer.objects.get(pk=customer_id)
    context = {"customer": customer, "orders": orders, **dates}
    return render(request, "core/customer.html", context)


def customer_daily_defaults(request, customer_id, date=None):
    dates = get_dates(date)
    if request.method == "POST":
        save_customer_daily_defaults(request, customer_id)
        return HttpResponseRedirect(reverse("core:index"))
    customer = Customer.objects.get(pk=customer_id)
    query = """
        SELECT b.name, b.id, IFNULL(dd.number, 0) AS number FROM core_bread b
        LEFT OUTER JOIN core_dailydefaults dd
        ON dd.bread_id = b.id AND dd.customer_id = %s
        ORDER BY number DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [customer_id])
        daily_defaults = cursor.fetchall()
    context = {"customer": customer, "daily_defaults": daily_defaults, **dates}
    return render(request, "core/customer_daily_defaults.html", context)
