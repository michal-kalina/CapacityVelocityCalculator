from django.db import models
from django.urls import reverse

# Create your models here.
class Person(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)

    def get_absolute_url(self):
        return reverse('person:detail', kwargs={'pk': self.pk})
        
    def __str__(self) -> str:
        return f"{self.name} {self.surname}"