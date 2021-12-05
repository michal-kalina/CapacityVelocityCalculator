from typing import Iterator
from .models import SprintCapacityPresenceItem, SprintCapacity, Sprint
from django.http import Http404
from django.db.models import QuerySet
from datetime import datetime, timedelta
from django.utils.functional import cached_property

class OutputItemPresenceDto:
    def __init__(self, id: int, date: datetime, presence: SprintCapacityPresenceItem.PRESENCE_CHOICES) -> None:
        self.id: int = id
        self.date: datetime = date
        self.presence: SprintCapacityPresenceItem.PRESENCE_CHOICES = presence

class OutputItemDto:
    def __init__(self, id: int , person_id: int, person_name: str, data: list[OutputItemPresenceDto]) -> None:
        self.id: int = id
        self.person_id: int = person_id
        self.person_name: str = person_name
        self.data: list[OutputItemPresenceDto] = data if data is not None else list()

    def __str__(self) -> str:
        s = ""
        for d in self.data:
            s += f"{d.date} "
        return f"<{self.id} {self.person_id}, {self.person_name} data: [{s}]>"

class OutputDto:
    def __init__(self, sprint_id: int, set_dummy_data: bool = False) -> None:
        self.sprint_id: int = sprint_id
        self.sprint_name: str = ''
        self.from_date = None
        self.to_date = None
        self.items: list[OutputItemDto] = list[OutputItemDto]()
        self._set_dummy_data = set_dummy_data
        self.get_data(sprint_id)
    
    def __str__(self) -> str:
        s = ""
        for i in self.items:
            s += f"{i} "
        return f"<{self.sprint_id} {self.sprint_name}, items: [{s}]>"

    @cached_property
    def size(self) -> int:
        """Number of elements it 'items' list"""
        return len(self.items)

    def create_date_ranges(self, start: datetime, end: datetime, **interval) -> Iterator[datetime]:
        """
        Examples:
        ('2021-11-15:00:00:00', '2021-11-17:13:00:00', {'days': 1}),
        ('2021-11-15:00:00:00', '2021-11-16:13:00:00', {'hours': 12}),
        ('2021-11-15:00:00:00', '2021-11-15:01:45:00', {'minutes': 30}),
        ('2021-11-15:00:00:00', '2021-11-15:00:01:12', {'seconds': 30})
        """
        start_ = start
        while start_ <= end:
            end_ = start_ + timedelta(**interval)
            yield start_
            start_ = end_

    def empty_item(self) -> OutputItemDto:
        data: list[OutputItemPresenceDto] = list[OutputItemPresenceDto]()
        for date in list(self.create_date_ranges(self.from_date, self.to_date, **{'days': 1})):
            data.append(OutputItemPresenceDto(0, date, SprintCapacityPresenceItem.PRESENCE_CHOICES[1]))
        
        outputItem = OutputItemDto(0, 0, "<unknown>", data)
        return outputItem

    def append_empty_item(self) -> OutputItemDto:
        outputItem = self.empty_item()
        self.items.append(outputItem)
        return outputItem

    def get_dummy_data_for(self) -> list[OutputItemPresenceDto]:
        data: list[OutputItemPresenceDto] = list[OutputItemPresenceDto]()
        for date in list(self.create_date_ranges(self.from_date, self.to_date, **{'days': 1})):
            data.append(OutputItemPresenceDto(0, date, SprintCapacityPresenceItem.PRESENCE_CHOICES[1]))
            
        return data

    def remove_at(self, index: int) -> None:
        if index in self.items:
            self.items.pop(index)

    def get_data(self, sprint_id) -> None:
        try:
            sprint: QuerySet[Sprint] = Sprint.objects.get(id=sprint_id)
            self.sprint_name = sprint.name
            self.from_date = sprint.from_date
            self.to_date = sprint.to_date
        except Sprint.DoesNotExist:
            raise Http404(f'There is no sprint with if {sprint_id}')

        current_sprint_capacities: QuerySet[SprintCapacity] = SprintCapacity.objects.filter(sprint__id=sprint.id)
        for capacity in current_sprint_capacities:
            # Init arrays
            data: list[OutputItemPresenceDto] = list[OutputItemPresenceDto]()

            if self._set_dummy_data:
                data = self.get_dummy_data_for()
            else:
                # Get person and its presences
                presences: QuerySet[SprintCapacityPresenceItem] = SprintCapacityPresenceItem.objects.filter(sprint_capacity__id=capacity.id).order_by('date')

                # Convert it to DTO lists
                for presence in presences:
                    data.append(OutputItemPresenceDto(presence.id, presence.date, presence.presence))

            self.items.append(OutputItemDto(capacity.id,capacity.person.id,f'{capacity.person.name} {capacity.person.surname}', data))