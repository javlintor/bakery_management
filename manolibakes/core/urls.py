from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("pedidos/<str:date>", views.index, name="pedidos"),
    path("clientes/<str:date>", views.customers, name="clientes"),
    path("panes/<str:date>", views.breads, name="panes"),
    path("cliente/<int:customer_id>/<str:date>", views.customer, name="cliente"),
    path(
        "cliente/valores_defecto_diarios/<int:customer_id>",
        views.customer_daily_defaults,
        name="cliente_valores_defecto_diarios",
    ),
]
