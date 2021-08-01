from capacity.capacity import Capacity
from capacity.people import Person, PresentItem
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

    def test_capacity_create_empty_dict_of_people(self):
        # Arrange
        # Act
        actual = Capacity({})

        # Assert
        assert len(actual.get_people()) == 0

    def test_capacity_create_raise_exception(self):
        with pytest.raises(TypeError, match=r"Unknown type for '.*?' arg") as exception_info:
            # Arrange
            # Act
            actual = Capacity(None)
            # Assert


    def test_capacity_create_with_people(self):
        # Arrange
        expected = None

        # Act
        actual = Capacity({"example": Person(None, None)})

        # Assert
        assert len(actual.get_people()) == 1

    def test_capacity_iterate_people(self):
        # Arrange
        # Act
        person1 = Person("John1", "Dou1")
        person2 = Person("John2", "Dou2")
        actual = Capacity([person1, person2])

        # Assert
        for item in actual:
            #assert item is Person
            assert re.search("John\\d", item.name) is not None
            assert re.search("Dou\\d", item.surname) is not None
            assert len(actual.get_people()) == 2

    def test_capacity_add_person(self):
        # Arrange
        person1 = Person("John1", "Dou1")
        person2 = Person("John2", "Dou2")
        actual = Capacity([person1, person2])

        # Act
        actual.add_person(Person("John3", "Dou3"))
        # Assert
        assert len(actual.get_people()) == 3
        for item in actual:
            #assert item is Person
            assert re.search("John\\d", item.name) is not None
            assert re.search("Dou\\d", item.surname) is not None


    def test_capacity_set_presence(self):
        # Arrange
        actual_start_datetime = datetime.strptime("2021-07-19", "%Y-%m-%d")
        actualPerson = Person("John", "Dou", actual_start_datetime, 2)
        actualPersonKey = actualPerson.key
        actual = Capacity([actualPerson])
        assert actual.get_people()[actualPersonKey].presents["2021-07-20"].present == True

        # Act
        actual.set_presence(actualPersonKey, "2021-07-20", False)

        # Assert
        assert actual.get_people()[actualPersonKey].presents["2021-07-20"].present == False


    @pytest.fixture
    def get_person_data(self,) -> Person:
        def _get_person_data(date: str, lp: int, days: int) -> Person:
            def _str_to_datetime(date: str) -> datetime:
                return datetime.strptime(date, "%Y-%m-%d")

            def _generate_days(_date: datetime, _days: int) -> list[datetime]:
                return [(_date + timedelta(days=day)) for day in range(0,_days)]
            
            person = Person(f"John{lp}", f"Dou{lp}", _str_to_datetime(date), 14) #14 days
            for day in _generate_days(_str_to_datetime(date), days):
                person.presents = PresentItem.Create(day, False)

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
        ("2021-07-19", [], 0.0),
    ])
    def test_people_parametrized(self, get_capacity_data, test_date, test_data, expected_capacity_percentage):

        # Arrange
        capacity: Capacity = get_capacity_data(test_date, test_data)

        # Act
        actual_calculated_presence = capacity.calculate_presence()

        # Assert
        assert actual_calculated_presence == expected_capacity_percentage


    @pytest.mark.parametrize(["test_date", "test_data", "actual_velocity_sp", "expect_velocity_sp"], [
        ("2021-07-19", [], 50, 0), #0%
        ("2021-07-19", [{"lp": 1, "days": 14}, {"lp": 2, "days": 14}], 50, 0), #0%
        ("2021-07-19", [{"lp": 1, "days": 9}, {"lp": 2, "days": 10}], 50, 12), #25%
        ("2021-07-19", [{"lp": 1, "days": 7}, {"lp": 2, "days": 7}], 50, 25), #50%
        ("2021-07-19", [{"lp": 1, "days": 2}, {"lp": 2, "days": 3}], 50, 38), #75%
        ("2021-07-19", [{"lp": 1, "days": 0}, {"lp": 2, "days": 0}], 50, 50), #100%
    ])
    def test_capacity_calculate_actual_capacity(self, get_capacity_data, test_date, test_data, actual_velocity_sp, expect_velocity_sp):
        # Arrange
        capacity: Capacity = get_capacity_data(test_date, test_data)

        # Act
        actual_calculated_presence: int = capacity.calculate_actual_capacity(actual_velocity_sp)

        # Assert
        assert actual_calculated_presence == expect_velocity_sp


