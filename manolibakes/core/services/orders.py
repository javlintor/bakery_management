from typing import TYPE_CHECKING

from core.dto import OrderDTO
from core.models import Bread, DailyDefaults, Order

if TYPE_CHECKING:
    import datetime


def _order_dto_sort_key(order_dto: OrderDTO) -> tuple[int, str]:
    return (-order_dto.number, order_dto.name)


def _build_orders_map(date: datetime.date) -> dict[tuple[int, int], int]:
    orders = Order.objects.filter(date=date).values("customer_id", "bread_id", "number")
    return {
        (order["customer_id"], order["bread_id"]): order["number"] for order in orders
    }


def _build_daily_defaults_map() -> dict[tuple[int, int], int]:
    daily_defaults = DailyDefaults.objects.values("customer_id", "bread_id", "number")
    return {
        (daily_default["customer_id"], daily_default["bread_id"]): daily_default[
            "number"
        ]
        for daily_default in daily_defaults
    }


def _sum_bread_totals(
    orders_map: dict[tuple[int, int], int],
    daily_defaults_map: dict[tuple[int, int], int],
) -> dict[int, int]:
    all_pairs = set(orders_map.keys()) | set(daily_defaults_map.keys())
    bread_totals: dict[int, int] = {}
    for customer_id, bread_id in all_pairs:
        default_number = daily_defaults_map.get((customer_id, bread_id), 0)
        resolved_number = orders_map.get((customer_id, bread_id), default_number)
        bread_totals[bread_id] = bread_totals.get(bread_id, 0) + resolved_number
    return bread_totals


def get_orders(date: datetime.date) -> list[OrderDTO]:
    orders_map = _build_orders_map(date=date)
    daily_defaults_map = _build_daily_defaults_map()
    bread_totals = _sum_bread_totals(
        orders_map=orders_map,
        daily_defaults_map=daily_defaults_map,
    )
    breads = list(Bread.objects.all())
    result = [
        OrderDTO(id=bread.id, name=bread.name, number=bread_totals.get(bread.id, 0))
        for bread in breads
    ]
    result.sort(key=_order_dto_sort_key)
    return result

