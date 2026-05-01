from django.db import models


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

    class Meta:
        verbose_name = "bread"
        verbose_name_plural = "breads"

    def __str__(self) -> str:
        return self.name


class WeeklyDefaults(models.Model):
    class Weekday(models.IntegerChoices):
        L = (0, "lunes")
        M = (1, "martes")
        X = (2, "miércoles")
        J = (3, "jueves")
        V = (4, "viernes")
        S = (5, "sábado")
        D = (6, "domingo")

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    weekday = models.PositiveIntegerField(choices=Weekday.choices)
    number = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["customer", "bread", "weekday"], name="unique-weekly-default"
            ),
        )

    def __str__(self) -> str:
        return (
            f"{self.customer} necesita {self.number} {self.bread} "
            f"el {self.Weekday(self.weekday).label}"
        )


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
