from django.db import models

# Create your models here.
class Person(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"