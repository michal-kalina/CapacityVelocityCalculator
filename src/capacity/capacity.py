from .people import People

class Capacity:
    def __init__(self, people:dict = dict()) -> None:
        if isinstance(people, dict):
            self.__people = people
        elif isinstance(people, list) and (len(people) > 0 and isinstance(people[0], tuple) and len(people[0]) == 2):
            self.__people = dict(people)
        else:
            raise TypeError("Unknown type for 'people' arg")
    
    def get_people(self) -> dict:
        return self.__people

    def add_person(self, new_person:People) -> None:
        key = new_person.Key()
        self.__people[key] = new_person

    def set_presence(self, key:str, date:str, value:bool) -> None:
        self.__people[key].presents[date].present = value

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