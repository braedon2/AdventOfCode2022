import pytest
from day2 import parse_strategy_guide, get_total_player_score, RockPaperScissorsRound

strategy_guide = """
A Y
B X
C Z
"""

def test_parse_strategy_guide():
    result = parse_strategy_guide(strategy_guide)
    assert result == [('A', 'Y'), ('B', 'X'), ('C', 'Z')]

def test_get_total_player_score():
    result = get_total_player_score(strategy_guide)
    assert result is 12

@pytest.mark.parametrize(
    "opponent,player,expected_score", [
    ('A', 'Y', 4),
    ('B', 'X', 1),
    ('C', 'Z', 7)
])
def test_get_player_score(opponent, player, expected_score):
    result = RockPaperScissorsRound(opponent, player).get_player_score()
    assert result is expected_score
