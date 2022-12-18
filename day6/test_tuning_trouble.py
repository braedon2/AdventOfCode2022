import pytest
from tuning_trouble import is_marker, find_marker


@pytest.mark.parametrize(
    "sequence,expectedResult", [
    ("asdf", True),
    ("aaaa", False),
    ("abac", False),
])
def test_is_marker(sequence, expectedResult):
    result = is_marker(sequence)

    assert result is expectedResult


@pytest.mark.parametrize(
    "buffer,expectedResult", [
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26)
])
def test_find_marker(buffer, expectedResult):
    result = find_marker(buffer)

    assert result is expectedResult
