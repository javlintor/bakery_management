import datetime
import io
from pathlib import Path
from typing import TYPE_CHECKING

from django.core.files.base import ContentFile
from django.utils.formats import date_format
from PIL import Image, ImageOps

if TYPE_CHECKING:
    from django.core.files.uploadedfile import UploadedFile
    from django.http import QueryDict


BREAD_IMAGE_MAX_DIMENSION = 800
BREAD_IMAGE_JPEG_QUALITY = 85


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


def resize_bread_image(uploaded_file: UploadedFile) -> ContentFile:
    uploaded_file.seek(0)
    pillow_image = Image.open(fp=uploaded_file)
    pillow_image = ImageOps.exif_transpose(image=pillow_image)
    if pillow_image.mode != "RGB":
        pillow_image = pillow_image.convert(mode="RGB")
    pillow_image.thumbnail(
        size=(BREAD_IMAGE_MAX_DIMENSION, BREAD_IMAGE_MAX_DIMENSION),
        resample=Image.Resampling.LANCZOS,
    )
    output_buffer = io.BytesIO()
    pillow_image.save(
        fp=output_buffer,
        format="JPEG",
        quality=BREAD_IMAGE_JPEG_QUALITY,
        optimize=True,
    )
    output_buffer.seek(0)
    original_stem = Path(uploaded_file.name).stem if uploaded_file.name else "image"
    output_name = f"{original_stem}.jpg"
    return ContentFile(content=output_buffer.read(), name=output_name)
