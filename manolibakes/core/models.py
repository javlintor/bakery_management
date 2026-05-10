from django.db import models

from core.fields import TitleCaseCharField


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
    name = TitleCaseCharField(max_length=200)
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
