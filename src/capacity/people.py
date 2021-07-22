from typing import Final, Type
from uuid import uuid1, UUID
from datetime import date, timedelta, datetime
from typing import Final

class PresentItem:
    def __init__(self, date: datetime) -> None:
        self.key: Final[str] = date.strftime("%Y-%m-%d")
        self.date: Final[datetime] = date
        self.work_day: Final[bool] = not date.weekday() in (5, 6) # 5 Saturday, 6 Sunday
        self.present = False if date.weekday() in (5, 6) else True

class People:
    def __init__(self, name:str, surname:str, starting_date:datetime=datetime.now(), period:int=14) -> None:
        self.name: Final[str] = name
        self.surname: Final[str] = surname
        self.__id: Final[UUID] = uuid1()
        self.__presents: Final[dict] = dict[str, PresentItem]()
        self.starting_date: Final[datetime] = starting_date
        for days in range(0, period):
            tmp_date = self.starting_date + timedelta(days=days)
            self.presents = PresentItem(tmp_date)

    @property
    def key(self) -> str:
        return f"{self.name}_{self.surname}_{self.__id}"

    @property
    def presents(self) -> dict[str, PresentItem]:
        return self.__presents

    @presents.setter
    def presents(self, value: PresentItem) -> None:
        self.__presents[value.key] = value

    def calculate_presence(self) -> float:
        if len(self.presents) == 0:
            return 0

        count = 0
        size = len(self.presents)
        for day in self.presents.values():
            count = count + (1 if (day.work_day and day.present == True) else 0)
            size = size + (-1 if not day.work_day else 0)
        
        return count / size
