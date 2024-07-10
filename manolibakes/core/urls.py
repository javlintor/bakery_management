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
    path("cliente/create", views.create_customer, name="crear-cliente"),
    path("cliente/edit/<int:customer_id>", views.edit_customer, name="editar-cliente"),
    path("cliente/delete/<int:customer_id>", views.delete_customer, name="borrar-cliente"),
]
