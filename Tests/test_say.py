import sys
# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, '../Src')

from Src.Say.say import say
import pytest

def expected_say():
    return 

def test_call_say():
    # Arrange
    expected = "something"

    # Act
    actual = say("something")

    # Assert
    assert actual == expected