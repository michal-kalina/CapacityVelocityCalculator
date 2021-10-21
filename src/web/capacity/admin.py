from django.contrib import admin

# Register your models here.
from .models import SprintCapacity, SprintCapacityPresenceItem

admin.site.register(SprintCapacity)
admin.site.register(SprintCapacityPresenceItem)