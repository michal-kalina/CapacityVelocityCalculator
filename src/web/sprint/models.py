from django.db import models
from django.urls import reverse

# Create your models here.
class Sprint(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)

    def get_absolute_url(self):
        return reverse('sprint:detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.name