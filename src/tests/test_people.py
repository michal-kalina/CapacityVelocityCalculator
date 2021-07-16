from capacity.people import People
import re

import pytest

def test_people_create_one() -> None:
    # Arrange
    expected = None

    # Act
    actual = People()

    # Assert
    assert actual is not expected


def test_people_create_one() -> None:
    # Arrange
    expectedName = "John"
    expectedSurName = "Dou"

    # Act
    actual = People("John", "Dou")

    # Assert
    assert actual.name == expectedName
    assert actual.surname == expectedSurName

def test_people_dic_key() -> None:
    # Arrange

    # Act
    actual = People("John", "Dou")

    # Assert
    match = re.search("John_Dou_[\\d\\w]{8}-[\\d\\w]{4}-[\\d\\w]{4}-[\\d\\w]{4}-[\\d\\w]{12}", actual.Key())
    assert match is not None