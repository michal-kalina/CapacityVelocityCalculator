from capacity.capacity import Capacity
from capacity.people import People
import re
from datetime import datetime

import pytest

def test_capacity_create_empty_list_of_people():
    # Arrange
    # Act
    actual = Capacity()

    # Assert
    assert len(actual.get_people()) == 0

def test_capacity_create_with_people():
    # Arrange
    expected = None

    # Act
    actual = Capacity({"example": People(None, None)})

    # Assert
    assert len(actual.get_people()) == 1

def test_capacity_iterate_people():
    # Arrange
    # Act
    person1 = People("John1", "Dou1")
    person2 = People("John2", "Dou2")
    actual = Capacity([(person1.Key(), person1), (person2.Key(), person2)])

    # Assert
    for item in actual:
        #assert item is People
        assert re.search("John\\d", item.name) is not None
        assert re.search("Dou\\d", item.surname) is not None
        assert len(actual.get_people()) == 2

def test_capacity_add_person():
    # Arrange
    person1 = People("John1", "Dou1")
    person2 = People("John2", "Dou2")
    actual = Capacity([(person1.Key(), person1), (person2.Key(), person2)])

    # Act
    actual.add_person(People("John3", "Dou3"))
    # Assert
    assert len(actual.get_people()) == 3
    for item in actual:
        #assert item is People
        assert re.search("John\\d", item.name) is not None
        assert re.search("Dou\\d", item.surname) is not None

def test_capacity_set_presence():
    # Arrange
    actual_start_datetime = datetime.strptime("2021-07-19", "%Y-%m-%d")
    actual_end_datetime = datetime.strptime("2021-07-26", "%Y-%m-%d") # + 7 days
    actualPerson =People("John", "Dou", actual_start_datetime, 7)
    actual = Capacity([("example_key", actualPerson)])

    # Act
    actual.set_presence("example_key", "2021-07-20", False)

    # Assert
    assert actual.get_people()["example_key"].presents["2021-07-20"].present == False