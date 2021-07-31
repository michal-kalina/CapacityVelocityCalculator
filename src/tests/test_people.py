from capacity.people import Person, PresentItem
import re
from datetime import date, datetime


def test_people_create_one() -> None:
    # Arrange
    expectedName = "John"
    expectedSurName = "Dou"
    expectedStarding:date = datetime.now()
    expectedSprintPeriod:int = 14

    # Act
    actual = Person(expectedName, expectedSurName, expectedStarding, expectedSprintPeriod)
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


def test_person_presence_create() -> None:
    # Arrange
    def _str_to_datetime(date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d")

    starting_date = _str_to_datetime("2021-07-19")
    change_data = _str_to_datetime("2021-07-20")
    expected_days = 7
    person = Person("John", "Dou", starting_date, expected_days)

    # Act
    person.presents = PresentItem.Create(change_data, False)

    # Assert
    assert len(person.presents) == expected_days
    assert person.presents["2021-07-19"].present == True # Monday
    assert person.presents["2021-07-20"].present == False # Tuesday
    assert person.presents["2021-07-21"].present == True # Wendsday
    assert person.presents["2021-07-22"].present == True # Thursday
    assert person.presents["2021-07-23"].present == True # Friday
    assert person.presents["2021-07-24"].present == False # Saturday
    assert person.presents["2021-07-25"].present == False # Sunday


def test_person_presence_create_presents_on_weekend_days_cant_be_alterate() -> None:
    # Arrange
    def _str_to_datetime(date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d")

    starting_date = _str_to_datetime("2021-07-19")
    saturday = _str_to_datetime("2021-07-24")
    sunday = _str_to_datetime("2021-07-24")
    expected_days = 7
    person = Person("John", "Dou", starting_date, expected_days)

    # Act
    person.presents = PresentItem.Create(saturday, False)
    person.presents = PresentItem.Create(sunday, False)

    # Assert
    assert len(person.presents) == expected_days
    assert person.presents["2021-07-19"].present == True # Monday
    assert person.presents["2021-07-20"].present == True # Tuesday
    assert person.presents["2021-07-21"].present == True # Wendsday
    assert person.presents["2021-07-22"].present == True # Thursday
    assert person.presents["2021-07-23"].present == True # Friday
    assert person.presents["2021-07-24"].present == False # Saturday
    assert person.presents["2021-07-25"].present == False # Sunday