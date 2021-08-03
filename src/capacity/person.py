from typing import Final, Type
from uuid import uuid1, UUID
from datetime import timedelta, datetime
from typing import Final


class PresentItem:
    def __init__(self, date: datetime) -> None:
        self.key: Final[str] = date.strftime("%Y-%m-%d")
        self.date: Final[datetime] = date
        self.work_day: Final[bool] = not date.weekday() in (
            5,  # Saturday
            6,  # Sunday
        )
        self.presence = False if date.weekday() in (5, 6) else True

    @staticmethod
    def Create(date: datetime, value: bool) -> "PresentItem":
        result = PresentItem(date)
        # T and T -> T
        # F and T -> F
        # T and F -> F
        # F and F -> F
        result.presence = value and result.work_day
        return result


class Person:
    def __init__(
        self,
        name: str,
        surname: str,
        starting_date: datetime = datetime.now(),
        period: int = 14,
    ) -> None:
        self.name: Final[str] = name
        self.surname: Final[str] = surname
        self.__id: Final[UUID] = uuid1()
        self.__presences: Final[dict] = dict[str, PresentItem]()
        self.starting_date: Final[datetime] = starting_date
        for days in range(0, period):
            tmp_date = self.starting_date + timedelta(days=days)
            self.presences = PresentItem(tmp_date)

    @property
    def key(self) -> str:
        return f"{self.name}_{self.surname}_{self.__id}"

    @property
    def presences(self) -> dict[str, PresentItem]:
        return self.__presences

    @presences.setter
    def presences(self, value: PresentItem) -> None:
        self.__presences[value.key] = value

    def calculate_presence(self) -> float:
        if len(self.presences) == 0:
            return 0

        count = 0
        size = len(self.presences)
        for day in self.presences.values():
            count = count + (1 if (day.work_day and day.presence == True) else 0)
            size = size + (-1 if not day.work_day else 0)

        return count / size
