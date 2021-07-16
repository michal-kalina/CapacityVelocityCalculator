from capacity.capacity import Capacity
from capacity.people import People

import pytest

def test_capacity():
    # Arrange
    expected = None

    # Act
    actual = Capacity()

    # Assert
    assert actual is not expected

def test_capacity_list_people():
    # Arrange
    # Act
    actual = Capacity()

    # Assert
    assert len(actual.GetPeople()) == 0

def test_capacity_create_with_people():
    # Arrange
    expected = None

    # Act
    actual = Capacity([People(None, None)])

    # Assert
    assert len(actual.GetPeople()) == 1