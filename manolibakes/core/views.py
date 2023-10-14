import datetime
from django.shortcuts import render
from .models import Order
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


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
    context = {
        "today_str": date_long_str,
        "orders": orders,
        "day_before_iso": day_before_iso,
        "day_after_iso": day_after_iso
    }
    return render(request, "core/index.html", context)
