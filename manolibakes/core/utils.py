import datetime

from django.http import QueryDict

_CSRF_TOKEN_KEY = "csrfmiddlewaretoken"


def extract_bread_quantities(post_data: QueryDict) -> list[tuple[int, int]]:
    result = []
    for key, value in post_data.items():
        if key == _CSRF_TOKEN_KEY:
            continue
        try:
            bread_id = int(key)
            quantity = int(value)
        except ValueError as error:
            raise ValueError(f"Invalid POST data: key={key}, value={value}") from error
        result.append((bread_id, quantity))
    return result


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
