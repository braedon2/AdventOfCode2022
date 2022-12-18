
def parse_strategy_guide(strategy_guide):
    return [
        tuple(line.split()) 
        for line in strategy_guide.strip().split('\n')
    ]

def get_total_player_score(strategy_guide):
    rounds = parse_strategy_guide(strategy_guide)
    scores = [
        RockPaperScissorsRound(_round[0], _round[1]).get_player_score()
        for _round in rounds 
    ]

    return sum(scores)

class RockPaperScissorsRound:
    shape_scores = {
        'A': 1,
        'X': 0,
        'B': 2,
        'Y': 3,
        'C': 3,
        'Z': 6
    }

    rules = {
        'A': 'C',
        'B': 'A',
        'C': 'B',
    }

    rule_complement = {
        'C': 'A',
        'A': 'B',
        'B': 'C'
    }

    def __init__(self, opponent_choice, outcome):
        self.opponent_choice = opponent_choice
        self.outcome = outcome

    def get_player_score(self):
        score = 0
        player_choice = None

        if self.outcome == 'X':
            player_choice = self.rules[self.opponent_choice]
        if self.outcome == 'Y':
            player_choice = self.opponent_choice
        if self.outcome == 'Z':
            player_choice = self.rule_complement[self.opponent_choice]

        return self.shape_scores[player_choice] + self.shape_scores[self.outcome]

    def get_opponent_score(self):
        score = 0

        if self.rules[self.opponent_choice] == self.player_choice:
            score += 6
        elif self.rules[self.player_choice] == self.opponent_choice:
            pass
        else:
            score += 3

        score += self.shape_scores[self.opponent_choice]
        return score 

if __name__ == "__main__":
    f = open("test_input", "r")
    strategy_guide = f.read()
    f.close
    print(get_total_player_score(strategy_guide))
