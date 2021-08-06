from velocity.velocity import Velocity, VelocityItem

import pytest

class TestVelocityCalculator:
    @pytest.fixture
    def get_velocity(self):
        return Velocity()
    
    @pytest.fixture
    def get_velocity_item(self):
        return VelocityItem()

    @pytest.mark.parametrize(
        ["context", "instance"],
        [
            [Velocity(), Velocity],
        ]
    )
    def test_create_instance_when_no_params_provided(self, context, instance):
        # Arrange
        # Act
        actual = context
        # Assert
        assert isinstance(context, instance)


    @pytest.mark.parametrize(
        ["sprint_name", "committed_sp", "compleated_sp", "capacity", "expected_calculated_velocity"],
        [
            ("Sprint 1", 100, 50, 1, 50),
            ("Sprint 2", 101, 51, 1, 51),
            ("Sprint 3", 10, 5, 0.000000000000000, 0),
            ("Sprint 3", 10, 5, 1.000000000000000, 5),
            ("Sprint 3", 10, 5, 0.8, 4),
        ]
    )
    def test_create_instance_with_params(self, sprint_name, committed_sp, compleated_sp, capacity, expected_calculated_velocity):
        # Arrange
        # Act
        actual = VelocityItem(sprint_name, committed_sp, compleated_sp, capacity)

        # Assert
        assert actual.sprint_name == sprint_name
        assert actual.committed_sp == committed_sp
        assert actual.compleated_sp == compleated_sp
        assert actual.capacity == capacity
        assert actual.calculate_velocity() == expected_calculated_velocity


    @pytest.mark.parametrize(
        ["invalid_capacity"],
        [
            [-0.000000000000001],
            [1.000000000000001],
        ]
    )
    def test_raise_error_when_invalid_value_passed(self, invalid_capacity):
        with pytest.raises(
            ValueError, match=r"Invalid valuse: .*?. The value should be between 0 and 1."
        ) as exception_info:
            # Arrange
            # Act
            actual = VelocityItem("dummy_sprint_name", 1, 1, invalid_capacity)
        # Assert