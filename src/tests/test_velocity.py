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
                    VelocityItem("Sprint 2", 120, 100, 0.95),
                ],
                95,
            ),
            (
                [
                    VelocityItem("Sprint 1", 120, 100, 0.8),  # 80
                    VelocityItem("Sprint 2", 120, 50, 0.5),  # 25
                    VelocityItem("Sprint 2", 120, 100, 0.75),  # 75
                ],
                60,
            ),
            (
                [],
                0,
            ),
            (
                [None, 0, "", 0.0, True, False],
                0,
            ),
            (
                [
                    VelocityItem("Sprint 0", 0, 0, 0),
                ],
                0,
            ),
            (
                [
                    VelocityItem("Sprint None", 0, 0, 1),
                ],
                0,
            ),
        ],
    )
    def test_calculate_velocity(self, velocity_item_data, expected_velocity):
        # Arrange
        velocity = Velocity(velocity_item_data)
        # Act
        actual_velocity = velocity.calculate_velocity()
        # Assert
        assert actual_velocity == expected_velocity

    def test_raise_error_when_invalid_data_passed(self):
        with pytest.raises(
            ValueError,
            match="'data' can't be None",
        ) as exception_info:
            # Arrange
            # Act
            actual = Velocity(None)
        # Assert
