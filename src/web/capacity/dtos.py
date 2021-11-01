from .models import SprintCapacityPresenceItem, SprintCapacity, Sprint, Person
from .forms import SprintCapacityUpdatePersonForm
from django.http import Http404
from django.db.models import QuerySet
from datetime import datetime

class OutputItemPresenceDto:
    def __init__(self, id: int, date: datetime, presence: SprintCapacityPresenceItem.PRESENCE_CHOICES) -> None:
        self.id: int = id
        self.date: datetime = date
        self.presence: SprintCapacityPresenceItem.PRESENCE_CHOICES = presence

class OutputItemDto:
    def __init__(self, person_name: str, person_form: SprintCapacityUpdatePersonForm, data: list[OutputItemPresenceDto]) -> None:
        self.person_name: str = person_name
        self.person_form: SprintCapacityUpdatePersonForm = person_form
        self.data: list[OutputItemPresenceDto] = data

class OutputDto:
    def __init__(self, sprint_id: int, persons_queryset: QuerySet[Person]) -> None:
        self.sprint_id = sprint_id
        self.sprint_name = ''
        self.items: list[OutputItemDto] = list[OutputItemDto]()
        self.person_queryset = persons_queryset
        self.get_data(sprint_id)

    def get_data(self, sprint_id) -> None:
        outputItemPresences: list[OutputItemPresenceDto] = None
        try:
            sprint: QuerySet[Sprint] = Sprint.objects.get(id=sprint_id)
            self.sprint_name = sprint.name
        except Sprint.DoesNotExist:
            raise Http404(f'There is no sprint with if {sprint_id}')
        current_sprint_capacities: QuerySet[SprintCapacity] = SprintCapacity.objects.filter(sprint__id=sprint.id)

        for capacity in current_sprint_capacities:
            print(capacity)
            # Init arrays
            outputItemPresences: list[OutputItemPresenceDto] = list[OutputItemPresenceDto]()

            # Get person and its presences
            presences: QuerySet[SprintCapacityPresenceItem] = SprintCapacityPresenceItem.objects.filter(sprint_capacity__id=capacity.id).order_by('date')

            # Convert it to DTO lists
            for presence in presences:
                outputItemPresences.append(OutputItemPresenceDto(presence.id, presence.date, presence.presence))
            self.items.append(OutputItemDto(f'{capacity.person.name} {capacity.person.surname}', outputItemPresences))