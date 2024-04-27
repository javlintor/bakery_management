from django.db import connection
from core.dto import OrderDTO


def get_orders(date: str) -> list[OrderDTO]:
    query = """
        SELECT
            b.name,
            b.id,
            COALESCE(COALESCE(o.number, dd.number), 0) AS number
        FROM core_bread b
        LEFT OUTER JOIN core_dailydefaults dd
        ON dd.bread_id = b.id
        LEFT OUTER JOIN core_order o
        ON o.bread_id = b.id AND o.date = %s
        ORDER BY number DESC, name;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [date])
        orders = cursor.fetchall()
    orders = [OrderDTO(name=order[0], id=order[1], number=order[2]) for order in orders]
    return orders
