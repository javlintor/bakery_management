from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from core.services.customer import (
    get_customer_final_orders,
    get_daily_defaults,
    save_customer_daily_defaults,
    save_customer_data,
)
from core.services.orders import get_orders

from .forms import BreadForm, CustomerForm
from .models import Bread, Customer, DailyDefaults
from .utils import get_dates

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required(login_url="members:login")
def index(request: HttpRequest) -> HttpResponse:
    date = request.GET.get("date")
    dates = get_dates(date)
    orders = get_orders(dates["date"])
    context = {"orders": orders, **dates}
    return render(request, "core/index.html", context)


@login_required(login_url="members:login")
def customers(request: HttpRequest) -> HttpResponse:
    customers = Customer.objects.all().order_by("name", "lastname")
    context = {"customers": customers}
    return render(request, "core/customers.html", context)


@login_required(login_url="members:login")
def breads(request: HttpRequest) -> HttpResponse:
    breads = Bread.objects.all().order_by("name")
    context = {"breads": breads}
    return render(request, "core/breads.html", context)


@login_required(login_url="members:login")
def customer(request: HttpRequest, customer_id: int, date: str | None = None) -> HttpResponse:
    if request.method == "POST":
        try:
            save_customer_data(request=request, customer_id=customer_id, date=date)
        except ValueError:
            return HttpResponseBadRequest()
        return HttpResponseRedirect(
            reverse(
                "core:cliente",
                kwargs={
                    "customer_id": customer_id,
                    "date": date,
                },
            )
        )
    date = request.GET.get("date")
    dates = get_dates(date)
    orders = get_customer_final_orders(customer_id, dates["date"])
    _customer = get_object_or_404(Customer, pk=customer_id)
    context = {"customer": _customer, "orders": orders, **dates}
    return render(request, "core/customer.html", context)


@login_required(login_url="members:login")
def customer_daily_defaults(request: HttpRequest, customer_id: int) -> HttpResponse:
    if request.method == "POST":
        try:
            save_customer_daily_defaults(request=request, customer_id=customer_id)
        except ValueError:
            return HttpResponseBadRequest()
        return HttpResponseRedirect(
            reverse(
                "core:cliente_valores_defecto_diarios",
                kwargs={"customer_id": customer_id},
            )
        )
    customer = get_object_or_404(Customer, pk=customer_id)
    daily_defaults = get_daily_defaults(customer_id)
    context = {"customer": customer, "daily_defaults": daily_defaults}
    return render(request, "core/customer_daily_defaults.html", context)


@login_required(login_url="members:login")
def create_customer(request: HttpRequest, date: str | None = None) -> HttpResponse:
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
def edit_customer(request: HttpRequest, customer_id: int, date: str | None = None) -> HttpResponse:
    dates = get_dates(date)
    customer = get_object_or_404(Customer, pk=customer_id)
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
def delete_customer(request: HttpRequest, customer_id: int) -> HttpResponse:
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return HttpResponseRedirect(reverse("core:clientes", kwargs={"date": None}))


@login_required(login_url="members:login")
def create_bread(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = BreadForm(
            {field: request.POST.getlist(field)[0] for field in request.POST}
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:panes"))
    context = {"form": BreadForm}
    return render(request, "core/create_bread.html", context)


@login_required(login_url="members:login")
def bread(request: HttpRequest, bread_id: int) -> HttpResponse:
    bread = get_object_or_404(Bread, pk=bread_id)
    if request.method == "POST":
        form = BreadForm(
            {field: request.POST.getlist(field)[0] for field in request.POST},
            instance=bread,
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:panes"))
    daily_defaults = list(
        DailyDefaults.objects.select_related("customer").filter(bread_id=bread_id)
    )
    total = sum(daily_default.number for daily_default in daily_defaults)
    context = {
        "form": BreadForm(instance=bread),
        "bread": bread,
        "total": total,
        "daily_defaults": daily_defaults,
    }
    return render(request, "core/bread.html", context)


@login_required(login_url="members:login")
def delete_bread(request: HttpRequest, bread_id: int) -> HttpResponse:
    bread = get_object_or_404(Bread, pk=bread_id)
    bread.delete()
    return HttpResponseRedirect(reverse("core:panes"))
