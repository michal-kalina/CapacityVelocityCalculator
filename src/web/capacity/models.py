from django.db import models
from datetime import timedelta, datetime

# Create your models here.
class Sprint(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name

class Person(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

class SprintCapacity(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True, default=None, related_name='sprint_capacity')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, default=None, related_name='sprint_capacity')
    velocity = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.id)

class SprintCapacityPresenceItem(models.Model):
    PRESENCE_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    sprint_capacity = models.ForeignKey(SprintCapacity, on_delete=models.CASCADE, null=True, default=None, related_name='sprint_capacity_presence')
    date = models.DateTimeField()
    presence = models.CharField(max_length=1, choices=PRESENCE_CHOICES)

    def __str__(self) -> str:
        return f"{self.date} {self.presence}"