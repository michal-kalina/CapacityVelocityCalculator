from django.contrib import admin

# Register your models here.
from .models import Person, SprintCapacity, SprintCapacityPresenceItem

admin.site.register(Person)
admin.site.register(SprintCapacity)
admin.site.register(SprintCapacityPresenceItem)