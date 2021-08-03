from datetime import datetime
from re import S
from .person import Person, PresentItem
from typing import Union


class Capacity:
    def __init__(self, persons: Union[list[Person], dict[str, Person]]) -> None:
        if isinstance(persons, dict):
            self.__persons = persons
        elif isinstance(persons, list):
            self.__persons = dict[str, Person]()
            for item in persons:
                self.__persons[item.key] = item
        else:
            raise TypeError("Unknown type for 'persons' arg")

    def get_persons(self) -> dict:
        return self.__persons

    def add_person(self, new_person: Person) -> None:
        self.__persons[new_person.key] = new_person

    def set_presence(self, key: str, date: str, value: bool) -> None:
        self.__persons[key].presences = PresentItem.Create(
            datetime.strptime(date, "%Y-%m-%d"), value
        )

    def calculate_presence(self):
        if len(self.__persons) == 0:
            return 0

        count = 0
        for persons in self.__persons.values():
            count = count + persons.calculate_presence()

        return count / len(self.__persons)

    def calculate_actual_capacity(self, velocity_sp: int) -> int:
        presence = self.calculate_presence()
        return round(velocity_sp * presence)

    def __iter__(self) -> None:
        self.__iterIndex = 0
        return self

    def __next__(self) -> None:
        if self.__iterIndex == len(self.__persons):
            raise StopIteration  # signals "the end"
        keys = list(self.__persons.keys())
        element = self.__persons[keys[self.__iterIndex]]
        self.__iterIndex = self.__iterIndex + 1
        return element
