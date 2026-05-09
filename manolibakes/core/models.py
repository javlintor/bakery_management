from django.core.files.uploadedfile import UploadedFile
from django.db import models

from core.utils import resize_bread_image


class Customer(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200, default="")

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["name", "lastname"], name="unique-name-lastname"
            ),
        )

    def __str__(self) -> str:
        return f"{self.name} {self.lastname}"


class Bread(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="breads/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "bread"
        verbose_name_plural = "breads"

    def __str__(self) -> str:
        return self.name

    def save(self, *args: object, **kwargs: object) -> None:
        if self.image and isinstance(self.image.file, UploadedFile):
            resized_content = resize_bread_image(uploaded_file=self.image.file)
            self.image.save(
                name=resized_content.name,
                content=resized_content,
                save=False,
            )
        super().save(*args, **kwargs)

    @property
    def image_url(self) -> str | None:
        return self.image.url if self.image else None


class DailyDefaults(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["customer", "bread"], name="unique-daily-default"
            ),
        )

    def __str__(self) -> str:
        return f"{self.customer} necesita {self.number} {self.bread} todos los dias"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    date = models.DateField()
    number = models.PositiveIntegerField(default=0, null=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["customer", "bread", "date"], name="unique-order"
            ),
        )

    def __str__(self) -> str:
        return f"{self.customer} necesita {self.number} {self.bread} el {self.date}"
