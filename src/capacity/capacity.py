from .people import People

class Capacity:
    def __init__(self, people:list = []) -> None:
        self.__people = people
        pass
    
    def GetPeople(self) -> list:
        return self.__people



if __name__ == "__main__":
    pass