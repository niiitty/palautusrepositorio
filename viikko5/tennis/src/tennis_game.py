SCORE_CALLS = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}
DEUCE_LABEL = "Deuce"
ADVANTAGE_THRESHOLD = 4


class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1" or player_name == self.player1_name:
            self.player1_score += 1
        else:
            self.player2_score += 1

    def _equal_score(self):
        if self.player1_score == 0:
            score = "Love-All"
        elif self.player1_score == 1:
            score = "Fifteen-All"
        elif self.player1_score == 2:
            score = "Thirty-All"
        else:
            score = DEUCE_LABEL

        return score

    def _advantage_or_win(self):
        score_diff = self.player1_score - self.player2_score

        if score_diff == 1:
            score = "Advantage player1"
        elif score_diff == -1:
            score = "Advantage player2"
        elif score_diff >= 2:
            score = "Win for player1"
        else:
            score = "Win for player2"

        return score

    def _normal_score(self):
        score = f"{SCORE_CALLS[self.player1_score]}-{SCORE_CALLS[self.player2_score]}"
        return score

    def get_score(self):
        if self.player1_score == self.player2_score:
            score = self._equal_score()
        elif self.player1_score >= ADVANTAGE_THRESHOLD or self.player2_score >= ADVANTAGE_THRESHOLD:
            score = self._advantage_or_win()
        else:
            score = self._normal_score()

        return score
