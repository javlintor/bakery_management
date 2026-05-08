from typing import TYPE_CHECKING

from django import forms
from django.forms import ModelForm
from PIL import Image, UnidentifiedImageError

from .models import Bread, Customer

if TYPE_CHECKING:
    from django.core.files.uploadedfile import UploadedFile


BREAD_IMAGE_MAX_BYTES = 5 * 1024 * 1024
BREAD_IMAGE_ALLOWED_FORMATS = frozenset(("JPEG", "PNG", "WEBP"))


class CustomerForm(ModelForm):
    name = forms.CharField(label="Nombre", max_length=100)
    lastname = forms.CharField(label="Apellidos", max_length=100)

    class Meta:
        model = Customer
        fields = ["name", "lastname"]


class BreadForm(ModelForm):
    name = forms.CharField(label="Nombre", max_length=100)
    image = forms.ImageField(label="Imagen", required=False)

    class Meta:
        model = Bread
        fields = ["name", "image"]

    def clean_image(self) -> UploadedFile | None:
        uploaded_file = self.cleaned_data.get("image")
        if uploaded_file is None:
            return None
        if uploaded_file.size > BREAD_IMAGE_MAX_BYTES:
            raise forms.ValidationError(message="La imagen no puede superar 5 MB.")
        uploaded_file.seek(0)
        try:
            with Image.open(fp=uploaded_file) as pillow_image:
                detected_format = pillow_image.format
        except (UnidentifiedImageError, OSError) as error:
            raise forms.ValidationError(
                message="Formato no permitido. Usa JPEG, PNG o WebP.",
            ) from error
        finally:
            uploaded_file.seek(0)
        if detected_format not in BREAD_IMAGE_ALLOWED_FORMATS:
            raise forms.ValidationError(
                message="Formato no permitido. Usa JPEG, PNG o WebP.",
            )
        return uploaded_file
