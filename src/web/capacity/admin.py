from django.contrib import admin

# Register your models here.
from .models import Sprint, Person, SprintCapacity, SprintCapacityPresenceItem

admin.site.register(Sprint)
admin.site.register(Person)
admin.site.register(SprintCapacity)
admin.site.register(SprintCapacityPresenceItem)