from uuid import uuid1

class People:
    def __init__(self, name:str, surname:str) -> None:
        self.name = name
        self.surname = surname
        self.__id = uuid1()
        pass

    def Key(self) -> str:
        return f"{self.name}_{self.surname}_{self.__id}"
