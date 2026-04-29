from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "core"
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="core:pedidos"), name="index"),
    path("pedidos/", views.index, name="pedidos"),
    path("clientes/", views.customers, name="clientes"),
    path("clientes/<str:date>", views.customers, name="clientes"),
    path("panes/", views.breads, name="panes"),
    path("pan/<int:bread_id>", views.bread, name="pan"),
    path("pan/create", views.create_bread, name="crear-pan"),
    path("pan/delete/<int:bread_id>", views.delete_bread, name="borrar-pan"),
    path("cliente/<int:customer_id>", views.customer, name="cliente"),
    path("cliente/<int:customer_id>/<str:date>", views.customer, name="cliente"),
    path(
        "cliente/valores_defecto_diarios/<int:customer_id>",
        views.customer_daily_defaults,
        name="cliente_valores_defecto_diarios",
    ),
    path("cliente/create", views.create_customer, name="crear-cliente"),
    path("cliente/edit/<int:customer_id>", views.edit_customer, name="editar-cliente"),
    path(
        "cliente/delete/<int:customer_id>", views.delete_customer, name="borrar-cliente"
    ),
]
