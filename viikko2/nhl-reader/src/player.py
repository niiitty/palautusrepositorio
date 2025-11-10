class Player:
    def __init__(self, player):
        self.name = player['name']
        self.team = player['team']
        self.goals = player['goals']
        self.assists = player['assists']
        self.nationality = player['nationality']
        self.points = self.goals + self.assists

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {self.points:3}"

    def plass(self):
        pass
