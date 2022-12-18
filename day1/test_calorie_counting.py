import pytest
from calorie_counting import (
    parse_raw_inventory, 
    map_to_total_calories, 
    find_elf_with_most_calories,
    find_top_three_elves_with_most_calories
)

raw_inventory = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def test_parse_raw_inventory():
    result = parse_raw_inventory(raw_inventory)
    expected_result = [[1000, 2000, 3000], [4000], [5000, 6000], [7000, 8000, 9000], [10000]]
    assert result == expected_result

def test_map_to_total_calories():
    result = map_to_total_calories([[1000, 2000, 3000], [4000], [5000, 6000], [7000, 8000, 9000], [10000]])
    assert result == [6000, 4000, 11000, 24000, 10000]

def test_find_elf_with_most_calories():
    result = find_elf_with_most_calories(raw_inventory)
    assert result == 24000

def test_find_top_three_elves_with_most_calories():
    result = find_top_three_elves_with_most_calories(raw_inventory)
    assert result == 45000
