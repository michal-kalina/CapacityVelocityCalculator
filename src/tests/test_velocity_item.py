from velocity.velocity import VelocityItem

import pytest


class TestVelocityItemCalculator:
    @pytest.mark.parametrize(
        [
            "sprint_name",
            "committed_sp",
            "compleated_sp",
            "capacity",
            "expected_calculated_velocity",
        ],
        [
            ("Sprint 1", 10, 5, 0.000000000000000, 0),  # The smallest amount
            ("Sprint 2", 10, 5, 1.000000000000000, 5),  # The highest amount
            ("Sprint 3", 10, 5, 0.5, 2),  # 50%
            ("Anything", 0, 0, 1, 0),
        ],
    )
    def test_create_instance_with_params(
        self,
        sprint_name,
        committed_sp,
        compleated_sp,
        capacity,
        expected_calculated_velocity,
    ):
        # Arrange
        # Act
        actual = VelocityItem(sprint_name, committed_sp, compleated_sp, capacity)

        # Assert
        assert actual.sprint_name == sprint_name
        assert actual.committed_sp == committed_sp
        assert actual.compleated_sp == compleated_sp
        assert actual.capacity == capacity
        assert actual.velocity == expected_calculated_velocity

    def test_sets_default_when_pass_invalid_values(self):
        # Arrange
        # Act
        actual = VelocityItem(None, None, None, 1)

        # Assert
        assert actual.sprint_name == "None sprint name was provided."
        assert actual.committed_sp == 0
        assert actual.compleated_sp == 0
        assert actual.capacity == 1
        assert actual.velocity == 0

    @pytest.mark.parametrize(
        ["invalid_capacity"],
        [[-0.000000000000001], [1.000000000000001], [None]],
    )
    def test_raise_error_when_invalid_value_passed(self, invalid_capacity):
        with pytest.raises(
            ValueError,
            match=r"Invalid valuse: .*?. The value should be between 0 and 1.",
        ) as exception_info:
            # Arrange
            # Act
            actual = VelocityItem("dummy_sprint_name", 1, 1, invalid_capacity)
        # Assert
