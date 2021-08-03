from capacity.person import Person, PresentItem
import re
from datetime import date, datetime
import pytest


def test_people_create_one() -> None:
    # Arrange
    expectedName = "John"
    expectedSurName = "Dou"
    expectedStarding: date = datetime.now()
    expectedSprintPeriod: int = 14

    # Act
    actual = Person(
        expectedName, expectedSurName, expectedStarding, expectedSprintPeriod
    )
    match = re.search(
        "John_Dou_[\\d\\w]{8}-[\\d\\w]{4}-[\\d\\w]{4}-[\\d\\w]{4}-[\\d\\w]{12}",
        actual.key,
    )

    # Assert
    assert actual.name == expectedName
    assert actual.surname == expectedSurName
    assert actual.starting_date == expectedStarding
    assert match is not None
    assert len(actual.presences) == expectedSprintPeriod
    for key in actual.presences.keys():
        item = actual.presences[key]
        assert item.date is not None
        if item.work_day:
            assert item.presence == True
        else:
            assert item.presence == False


def test_person_presence_create(str_to_datetime) -> None:
    # Arrange
    starting_date = str_to_datetime("2021-07-19")
    change_data = str_to_datetime("2021-07-20")
    expected_days = 7
    person = Person("John", "Dou", starting_date, expected_days)

    # Act
    person.presences = PresentItem.Create(change_data, False)

    # Assert
    assert len(person.presences) == expected_days
    assert person.presences["2021-07-19"].presence == True  # Monday
    assert person.presences["2021-07-20"].presence == False  # Tuesday
    assert person.presences["2021-07-21"].presence == True  # Wendsday
    assert person.presences["2021-07-22"].presence == True  # Thursday
    assert person.presences["2021-07-23"].presence == True  # Friday
    assert person.presences["2021-07-24"].presence == False  # Saturday
    assert person.presences["2021-07-25"].presence == False  # Sunday


def test_person_presence_create_presences_on_weekend_days_cant_be_alterate(
    str_to_datetime,
) -> None:
    # Arrange
    starting_date = str_to_datetime("2021-07-19")
    saturday = str_to_datetime("2021-07-24")
    sunday = str_to_datetime("2021-07-24")
    expected_days = 7
    person = Person("John", "Dou", starting_date, expected_days)

    # Act
    person.presences = PresentItem.Create(saturday, False)
    person.presences = PresentItem.Create(sunday, False)

    # Assert
    assert len(person.presences) == expected_days
    assert person.presences["2021-07-19"].presence == True  # Monday
    assert person.presences["2021-07-20"].presence == True  # Tuesday
    assert person.presences["2021-07-21"].presence == True  # Wendsday
    assert person.presences["2021-07-22"].presence == True  # Thursday
    assert person.presences["2021-07-23"].presence == True  # Friday
    assert person.presences["2021-07-24"].presence == False  # Saturday
    assert person.presences["2021-07-25"].presence == False  # Sunday


@pytest.fixture
def str_to_datetime():
    def _str_to_datetime(date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d")

    return _str_to_datetime


@pytest.mark.parametrize(
    ["days", "expected_calculate_presence"], [(0, 0), (1, 1), (14, 1)]
)
def test_person_calculate_presence(str_to_datetime, days, expected_calculate_presence):
    # Arrange

    starting_date = str_to_datetime("2021-07-19")
    # Act
    person = Person("John", "Dou", starting_date, days)

    # Assert
    assert person.calculate_presence() == expected_calculate_presence
