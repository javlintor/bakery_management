import datetime


def get_post_data(request):
    data = str(request.body).replace("'", "").split("&")[1:]
    data = [d.split("=") for d in data]
    return data


def get_dates(date_str: str | None = None) -> dict:
    if date_str is None:
        date = datetime.date.today() + datetime.timedelta(days=1)
    else:
        try:
            date = datetime.date.fromisoformat(date_str)
        except ValueError:
            date = datetime.date.today() + datetime.timedelta(days=1)
    date_long_str = date.strftime("%A, %d de %B de %Y")
    date_iso_str = date.strftime("%Y-%m-%d")
    return {
        "date": date,
        "date_iso_str": date_iso_str,
        "date_long_str": date_long_str,
    }
