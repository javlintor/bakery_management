import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from .models import Order, Customer, Bread
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
    customers = Customer.objects.all().order_by('name', 'lastname')
    context = {"customers": customers, **dates}
    return render(request, "core/customers.html", context)


def breads(request, date=None):
    dates = get_dates(date)
    breads = Bread.objects.all()
    context = {"breads": breads, **dates}
    return render(request, "core/breads.html", context)


def save_customer_data(request, customer_id, date):
    data = str(request.body).replace("'", '').split('&')[1:]
    data = [d.split('=') for d in data]
    for bread_id, number in data:
        order = Order.objects.get(customer_id=customer_id, date=date, bread_id=bread_id)
        order.number = int(number)
        order.save()


def customer(request, customer_id, date):
    if request.method == "POST":
        save_customer_data(request, customer_id, date)
        return HttpResponseRedirect(reverse("core:index"))
    dates = get_dates(date)
    orders = Order.objects.filter(customer_id=customer_id, date=dates["date"])
    customer = Customer.objects.get(pk=customer_id)
    context = {"customer": customer, "orders": orders, **dates}
    return render(request, "core/customer.html", context)


def test(request):
    date = '2024-01-06'
    dates = get_dates(date)
    context = {**dates}
    return render(request, "core/test.html", context)
