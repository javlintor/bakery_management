from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} {self.lastname}"


class Bread(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class WeeklyDefaults(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=20)
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.customer} necesita {self.number} {self.bread} los {self.weekday}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "bread", "weekday"], name="unique-weekly-default"
            )
        ]


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE)
    date = models.DateField()
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.customer} needs {self.number} {self.bread} on {self.date}"
