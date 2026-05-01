import datetime
from typing import TYPE_CHECKING

from django.utils.formats import date_format

if TYPE_CHECKING:
    from django.http import QueryDict


def extract_bread_quantities(post_data: QueryDict) -> list[tuple[int, int]]:
    result = []
    for key, value in post_data.items():
        if key == "csrfmiddlewaretoken":
            continue
        try:
            bread_id = int(key)
            quantity = int(value)
        except ValueError as error:
            raise ValueError(f"Invalid POST data: key={key}, value={value}") from error
        result.append((bread_id, quantity))
    return result


class DateResolver:
    _DATE_FORMAT_STR = r"l, j \d\e F \d\e Y"

    def __init__(self, date_str: str | None = None) -> None:
        self._date = self._resolve_date(date_str=date_str)

    def _resolve_date(self, date_str: str | None) -> datetime.date:
        if date_str is None:
            return datetime.datetime.now(tz=datetime.UTC).date() + datetime.timedelta(
                days=1
            )
        try:
            return datetime.date.fromisoformat(date_str)
        except ValueError:
            return datetime.datetime.now(tz=datetime.UTC).date() + datetime.timedelta(
                days=1
            )

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def date_iso_str(self) -> str:
        return self._date.strftime("%Y-%m-%d")

    @property
    def date_long_str(self) -> str:
        return date_format(value=self._date, format=self._DATE_FORMAT_STR)
