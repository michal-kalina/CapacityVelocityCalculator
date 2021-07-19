from uuid import uuid1
from datetime import date, timedelta, datetime

class PresentItem:
    def __init__(self, date:date) -> None:
        self.date = date
        self.present = False if date.weekday() in (5, 6) else True
        self.work_day = not date.weekday() in (5, 6) # 5 Saturday, 6 Sunday

class People:
    def __init__(self, name:str, surname:str, starting_date:datetime=datetime.now(), period:int=14) -> None:
        self.name = name
        self.surname = surname
        self.__id = uuid1()
        self.presents = dict()
        self.starting_date = starting_date
        for days in range(0, period):
            tmp_date = self.starting_date + timedelta(days=days)
            key = tmp_date.strftime("%Y-%m-%d")
            self.presents[key] = PresentItem(tmp_date)

    def Key(self) -> str:
        return f"{self.name}_{self.surname}_{self.__id}"
