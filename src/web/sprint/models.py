from django.db import models
from django.urls import reverse
import datetime

# Create your models here.
class Sprint(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)
    from_date = models.DateField('From', default=datetime.date.today)
    to_date = models.DateField('To', default=datetime.date.today)

    def get_absolute_url(self):
        return reverse('sprint:detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.name