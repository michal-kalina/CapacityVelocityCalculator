from velocity.velocity import Velocity, VelocityItem

import pytest


class TestVelocityItemCalculator:
    @pytest.mark.parametrize(
        ["context", "instance"],
        [
            [Velocity([]), Velocity],
        ],
    )
    def test_create_instance_when_no_params_provided(self, context, instance):
        # Arrange
        # Act
        actual = context
        # Assert
        assert isinstance(context, instance)

    @pytest.mark.parametrize(
        ["velocity_item_data", "expected_velocity"],
        [
            (
                [
                    VelocityItem("Sprint 1", 120, 100, 0.95),
                    VelocityItem("Sprint 1", 120, 100, 0.95),
                ],
                95,
            )
        ],
    )
    def test_calculate_velocity(self, velocity_item_data, expected_velocity):
        # Arrange
        velocity = Velocity(velocity_item_data)
        # Act
        actual_velocity = velocity.calculate_velocity()
        # Assert
        assert actual_velocity == expected_velocity
