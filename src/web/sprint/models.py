from django.db import models

# Create your models here.
class Sprint(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name