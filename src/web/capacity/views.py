from typing import Tuple
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.db.models import QuerySet
from .models import Person, SprintCapacity, Sprint, SprintCapacityPresenceItem

from datetime import datetime

class OutputItemPresenceDto:
    def __init__(self, id:int, date: datetime, presence: SprintCapacityPresenceItem.PRESENCE_CHOICES) -> None:
        self.id: int = id
        self.date: datetime = date
        self.presence: SprintCapacityPresenceItem.PRESENCE_CHOICES = presence

class OutputItemDto:
    def __init__(self, person_name: str, data: list[OutputItemPresenceDto]) -> None:
        self.person_name: str = person_name
        self.data: list[OutputItemPresenceDto] = data
        
class OutputStringDto:
    def __init__(self, id:str, name:str) -> None:
        self.id = id
        self.name = name

class OutputDto:
    def __init__(self, sprint_name: str, items: list[OutputItemDto]) -> None:
        self.sprint_name: str = sprint_name
        self.items: list[OutputItemDto] = items

def index(request):
    last_five_sprints: QuerySet[Sprint] = Sprint.objects.order_by("-id")[:5]
    output: list[OutputStringDto] = list[OutputStringDto]()
    for sprint in last_five_sprints:
        output.append(OutputStringDto(sprint.id, sprint.name))
    context = {
        'output': output,
    }
    return render(request, 'capacity/index.html', context)

# Create your views here.
def details(request, sprint_id):
    print(f'sprint id: {sprint_id}')
    outputItems: list[OutputItemDto] = list[OutputItemDto]()
    outputItemPresences: list[OutputItemPresenceDto] = None
    try:
        current_sprint: QuerySet[Sprint] = Sprint.objects.get(id=sprint_id)
    except Sprint.DoesNotExist:
        raise Http404("No sprint has been defined")
    current_sprint_capacities: QuerySet[SprintCapacity] = SprintCapacity.objects.filter(sprint__id=current_sprint.id)

    for capacity in current_sprint_capacities:
        print(capacity)
        # Init arrays
        outputItemPresences: list[OutputItemPresenceDto] = list[OutputItemPresenceDto]()

        # Get person and its presences
        #person: QuerySet[Person] = Person.objects.get(id=capacity.person.id)
        presences: QuerySet[SprintCapacityPresenceItem] = SprintCapacityPresenceItem.objects.filter(sprint_capacity__id=capacity.id).order_by('date')

        # Convert it to DTO lists
        for presence in presences:
            print(presence)
            outputItemPresences.append(OutputItemPresenceDto(presence.id, presence.date, presence.presence))
        outputItems.append(OutputItemDto(f'{capacity.person.name} {capacity.person.surname}', outputItemPresences))

    output = OutputDto(current_sprint.name, outputItems)
    context = {
        'output': output,
    }
    return render(request, 'capacity/details.html', context)

def update(request):
    print(request)
    if request.method == 'POST':
        id = request.POST['id']
        presence = request.POST['presence']
        date = request.POST['date']
        try:
            
            presenceItem: QuerySet[SprintCapacityPresenceItem] = get_object_or_404(SprintCapacityPresenceItem, id=id)
            if(presence in SprintCapacityPresenceItem.PRESENCE_CHOICES[0]): # Is in Yes tuple
                presenceItem.presence, _ = SprintCapacityPresenceItem.PRESENCE_CHOICES[1] # N
            else: # Is in no tuple
                presenceItem.presence, _ = SprintCapacityPresenceItem.PRESENCE_CHOICES[0] # Y
            presenceItem.save()
            sprint_id = presenceItem.sprint_capacity.sprint.id
            return redirect(reverse('capacity:details', kwargs={'sprint_id': sprint_id})) # We redirect to the same view
        except SprintCapacityPresenceItem.DoesNotExist as e:
            raise Http404(f"No SprintCapacityPresenceItem matches the given id: {id}.")
