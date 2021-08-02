from say.say import say
import pytest


def test_call_say():
    # Arrange
    expected = "something"

    # Act
    actual = say("something")

    # Assert
    assert actual == expected
