from datetime import date
from django.shortcuts import render
import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


def index(request):
    today = date.today().strftime('%A, %d de %B de %Y')
    context = {
        "date": today
    }
    return render(request, "core/index.html", context)
