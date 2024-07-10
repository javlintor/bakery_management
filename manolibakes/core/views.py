import datetime
from .forms import CustomerForm
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from .models import Customer, Bread
from core.services.customer import (
    get_daily_defaults,
    save_customer_daily_defaults,
    get_customer_final_orders,
    save_customer_data,
)
from core.services.orders import get_orders
import locale
import logging
from django.contrib.auth.decorators import login_required

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def get_dates(date_str: str | None = None) -> dict:
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


@login_required(login_url="members:login")
def index(request, date=None):
    dates = get_dates(date)
    orders = get_orders(dates["date"])
    context = {"orders": orders, **dates}
    return render(request, "core/index.html", context)


@login_required(login_url="members:login")
def customers(request, date=None):
    dates = get_dates(date)
    customers = Customer.objects.all().order_by("name", "lastname")
    context = {"customers": customers, **dates}
    return render(request, "core/customers.html", context)


@login_required(login_url="members:login")
def breads(request, date=None):
    dates = get_dates(date)
    breads = Bread.objects.all()
    context = {"breads": breads, **dates}
    return render(request, "core/breads.html", context)


@login_required(login_url="members:login")
def customer(request, customer_id, date):
    if request.method == "POST":
        save_customer_data(request, customer_id, date)
        return HttpResponseRedirect(
            reverse(
                "core:cliente",
                kwargs={
                    "customer_id": customer_id,
                    "date": date,
                },
            )
        )
    orders = get_customer_final_orders(customer_id, date)
    _customer = Customer.objects.get(pk=customer_id)
    dates = get_dates(date)
    context = {"customer": _customer, "orders": orders, **dates}
    return render(request, "core/customer.html", context)


@login_required(login_url="members:login")
def customer_daily_defaults(request, customer_id, date=None):
    dates = get_dates(date)
    if request.method == "POST":
        save_customer_daily_defaults(request, customer_id)
        return HttpResponseRedirect(
            reverse(
                "core:cliente_valores_defecto_diarios",
                kwargs={"customer_id": customer_id},
            )
        )
    customer = Customer.objects.get(pk=customer_id)
    daily_defaults = get_daily_defaults(customer_id)
    context = {"customer": customer, "daily_defaults": daily_defaults, **dates}
    return render(request, "core/customer_daily_defaults.html", context)


@login_required(login_url="members:login")
def create_customer(request, date=None):
    dates = get_dates(date)
    if request.method == "POST":
        form = CustomerForm(
            {field: request.POST.getlist(field)[0] for field in request.POST}
        )
        if form.is_valid():
            new_customer = form.save()
            return HttpResponseRedirect(
                reverse(
                    "core:cliente",
                    kwargs={
                        "customer_id": new_customer.id,
                        "date": date,
                    },
                )
            )
    context = {**dates, "form": CustomerForm}
    return render(request, "core/create_customer.html", context)


@login_required(login_url="members:login")
def edit_customer(request, customer_id: int, date=None):
    dates = get_dates(date)
    customer = Customer.objects.get(pk=customer_id)
    if request.method == "POST":
        form = CustomerForm(
            {field: request.POST.getlist(field)[0] for field in request.POST},
            instance=customer,
        )
        if form.is_valid():
            new_customer = form.save()
            return HttpResponseRedirect(
                reverse(
                    "core:cliente",
                    kwargs={
                        "customer_id": new_customer.id,
                        "date": date,
                    },
                )
            )
    context = {
        **dates,
        "form": CustomerForm(instance=customer),
        "customer_id": customer.id,
    }
    return render(request, "core/edit_customer.html", context)


@login_required(login_url="members:login")
def delete_customer(request, customer_id: int):
    customer = Customer.objects.get(pk=customer_id)
    customer.delete()
    return HttpResponseRedirect(reverse("core:clientes", kwargs={"date": None}))
