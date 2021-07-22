from capacity.capacity import Capacity
from capacity.people import People
import re
from datetime import datetime

import pytest

class TestCapacity:
    def test_capacity_create_empty_list_of_people(self):
        # Arrange
        # Act
        actual = Capacity([])

        # Assert
        assert len(actual.get_people()) == 0

    def test_capacity_create_with_people(self):
        # Arrange
        expected = None

        # Act
        actual = Capacity({"example": People(None, None)})

        # Assert
        assert len(actual.get_people()) == 1

    def test_capacity_iterate_people(self):
        # Arrange
        # Act
        person1 = People("John1", "Dou1")
        person2 = People("John2", "Dou2")
        actual = Capacity([person1, person2])

        # Assert
        for item in actual:
            #assert item is People
            assert re.search("John\\d", item.name) is not None
            assert re.search("Dou\\d", item.surname) is not None
            assert len(actual.get_people()) == 2

    def test_capacity_add_person(self):
        # Arrange
        person1 = People("John1", "Dou1")
        person2 = People("John2", "Dou2")
        actual = Capacity([person1, person2])

        # Act
        actual.add_person(People("John3", "Dou3"))
        # Assert
        assert len(actual.get_people()) == 3
        for item in actual:
            #assert item is People
            assert re.search("John\\d", item.name) is not None
            assert re.search("Dou\\d", item.surname) is not None

    def test_capacity_set_presence(self):
        # Arrange
        actual_start_datetime = datetime.strptime("2021-07-19", "%Y-%m-%d")
        actualPerson = People("John", "Dou", actual_start_datetime, 2)
        actualPersonKey = actualPerson.key
        actual = Capacity([actualPerson])
        assert actual.get_people()[actualPersonKey].presents["2021-07-20"].present == True

        # Act
        actual.set_presence(actualPersonKey, "2021-07-20", False)

        # Assert
        assert actual.get_people()[actualPersonKey].presents["2021-07-20"].present == False

    def test_capacity_calculate_full_presence_of_people(self):
        # Arrange
        actual_start_datetime = datetime.strptime("2021-07-19", "%Y-%m-%d") # it starts at Monday
        person1 =People("John1", "Dou2", actual_start_datetime, 14) #10 working days
        person2 =People("John2", "Dou2", actual_start_datetime, 14) #10 working days
        actual = Capacity([person1, person2])

        # Act
        actualCalculatedPresence = actual.calculate_presence()

        # Assert
        assert actualCalculatedPresence == 1.0

    def test_capacity_calculate_none_presence_of_people(self):
        # Arrange
        actual_start_datetime = datetime.strptime("2021-07-19", "%Y-%m-%d") # it starts at Monday
        person1 =People("John1", "Dou2", actual_start_datetime, 1) #1 working days
        person1.presents["2021-07-19"].present = False
        person2 =People("John2", "Dou2", actual_start_datetime, 1) #1 working days
        person2.presents["2021-07-19"].present = False
        capacity = Capacity([person1, person2])

        # Act
        actualCalculatedPresence = capacity.calculate_presence()

        # Assert
        assert actualCalculatedPresence == 0