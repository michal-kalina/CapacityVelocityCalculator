from re import S
from .people import People
from typing import Union

class Capacity:
    def __init__(self, people: Union[list[People], dict[str, People]]) -> None:
        if isinstance(people, dict):
            self.__people = people
        elif isinstance(people, list):
            self.__people = dict[str, People]()
            for item in people:
                self.__people[item.key] = item
        else:
            raise TypeError("Unknown type for 'people' arg")
    
    def get_people(self) -> dict:
        return self.__people

    def add_person(self, new_person:People) -> None:
        self.__people[new_person.key] = new_person

    def set_presence(self, key:str, date:str, value:bool) -> None:
        self.__people[key].presents[date].present = value

    def calculate_presence(self):
        if len(self.__people) == 0:
            return 0

        count = 0
        for person in self.__people.values():
            count = count + person.calculate_presence()

        return count / len(self.__people)

    def calculate_actual_capacity(self, velocity_sp:int) -> int:
        presence = self.calculate_presence()
        return round(velocity_sp * presence)

    def __iter__(self) -> None:
        self.__iterIndex = 0
        return self
    
    def __next__(self) -> None:
        if(self.__iterIndex == len(self.__people)):
            raise StopIteration  # signals "the end"
        keys = list(self.__people.keys())
        element = self.__people[keys[self.__iterIndex]]
        self.__iterIndex = self.__iterIndex + 1
        return element




if __name__ == "__main__":
    pass