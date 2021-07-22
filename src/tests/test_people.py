from capacity.people import People
import re
from datetime import date, datetime


def test_people_create_one() -> None:
    # Arrange
    expectedName = "John"
    expectedSurName = "Dou"
    expectedStarding:date = datetime.now()
    expectedSprintPeriod:int = 14

    # Act
    actual = People(expectedName, expectedSurName, expectedStarding, expectedSprintPeriod)
    match = re.search("John_Dou_[\\d\\w]{8}-[\\d\\w]{4}-[\\d\\w]{4}-[\\d\\w]{4}-[\\d\\w]{12}", actual.key)

    # Assert
    assert actual.name == expectedName
    assert actual.surname == expectedSurName
    assert actual.starting_date == expectedStarding
    assert match is not None
    assert len(actual.presents) == expectedSprintPeriod
    for key in actual.presents.keys():
        item = actual.presents[key]
        assert item.date is not None
        if(item.work_day):
            assert item.present == True
        else:
            assert item.present == False


def test_people_dic_key() -> None:
    # Arrange

    # Act
    actual = People("John", "Dou")

    # Assert
    pass