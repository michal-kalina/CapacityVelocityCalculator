from capacity.capacity import Capacity
from capacity.people import People
import re
from datetime import datetime, timedelta

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
        assert actualCalculatedPresence == 0.0


    def test_capacity_calculate_half_presence_of_people(self):
        # Arrange
        actual_start_datetime = datetime.strptime("2021-07-19", "%Y-%m-%d") # it starts at Monday
        person1 =People("John1", "Dou2", actual_start_datetime, 7) #7 working days
        person1.presents["2021-07-19"].present = False # Monday
        person1.presents["2021-07-20"].present = False # Tuesday
        person1.presents["2021-07-21"].present = False # Wednesday
        person2 =People("John2", "Dou2", actual_start_datetime, 7) #7 working days
        person2.presents["2021-07-22"].present = False # Tuesday
        person2.presents["2021-07-23"].present = False # Wednesday
        capacity = Capacity([person1, person2])

        # Act
        actualCalculatedPresence = capacity.calculate_presence()

        # Assert
        assert actualCalculatedPresence == 0.5

    @pytest.fixture
    def example_data_capacity_50(self) -> Capacity:
        actual_start_datetime = datetime.strptime("2021-07-19", "%Y-%m-%d") # it starts at Monday
        person1 =People("John1", "Dou2", actual_start_datetime, 7) #7 working days
        person1.presents["2021-07-19"].present = False # Monday
        person1.presents["2021-07-20"].present = False # Tuesday
        person1.presents["2021-07-21"].present = False # Wednesday
        person2 =People("John2", "Dou2", actual_start_datetime, 7) #7 working days
        person2.presents["2021-07-22"].present = False # Tuesday
        person2.presents["2021-07-23"].present = False # Wednesday
        return Capacity([person1, person2])

    @pytest.fixture
    def get_person_data(self,) -> People:
        def _get_person_data(date: str, lp: int, days: int) -> People:
            def _str_to_datetime(date: str) -> datetime:
                return datetime.strptime(date, "%Y-%m-%d")

            def _generate_days(_date: datetime, _days: int) -> list[str]:
                return [(_date + timedelta(days=day)).strftime("%Y-%m-%d") for day in range(0,_days)]
            
            person = People(f"John{lp}", f"Dou{lp}", _str_to_datetime(date), 14) #14 days
            for day in _generate_days(datetime.strptime(date, "%Y-%m-%d"), days):
                person.presents[day].present = False

            return person
        
        return _get_person_data

    @pytest.fixture
    def get_capacity_data(self, get_person_data) -> list[Capacity]:
        def _get_capacity_data(date: str, data: list[dict[str, int]]) -> list[Capacity]:
            return Capacity([get_person_data(date, d["lp"], d["days"]) for d in data])

        return _get_capacity_data

    @pytest.mark.parametrize(["test_date", "test_data", "expected_capacity_percentage"], [
        ("2021-07-19", [{"lp": 1, "days": 2}, {"lp": 2, "days": 3}], 0.75), # people are appsent for 5 days out of 20 which is 0.75 capacity percentage
        ("2021-07-19", [{"lp": 1, "days": 5}, {"lp": 2, "days": 5}], 0.5),
        ("2021-07-19", [{"lp": 1, "days": 0}, {"lp": 2, "days": 0}], 1.0),
        ("2021-07-19", [{"lp": 1, "days": 14}, {"lp": 2, "days": 14}], 0.0),
    ])
    def test_people_parametrized(self, get_capacity_data, test_date, test_data, expected_capacity_percentage):

        # Arrange
        capacity: Capacity = get_capacity_data(test_date, test_data)

        # Act
        actual_calculated_presence = capacity.calculate_presence()

        # Assert
        assert actual_calculated_presence == expected_capacity_percentage


    @pytest.mark.parametrize(["example_data_capacity", "actual_velocity_sp", "expect_velocity_sp"], [
        (pytest.lazy_fixture("example_data_capacity_50"), 50, 25)
    ])
    def test_capacity_calculate_actual_capacity(self, example_data_capacity, actual_velocity_sp, expect_velocity_sp):
        # Arrange
        capacity: Capacity = example_data_capacity

        # Act
        actualCalculatedPresence: int = capacity.calculate_actual_capacity(actual_velocity_sp)

        # Assert
        assert actualCalculatedPresence == expect_velocity_sp


