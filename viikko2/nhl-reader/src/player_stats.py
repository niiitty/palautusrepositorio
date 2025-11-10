class PlayerStats:
    def __init__(self, reader):
        self._players = reader.get_players()

    def get_players(self):
        return self._players

    def top_scorers_by_nationality(self, nationality):
        filtered_players = filter(
            lambda player: player.nationality == nationality,
            self._players
        )

        filtered_players = sorted(
            filtered_players,
            key=lambda player: player.goals + player.assists,
            reverse=True
        )

        return filtered_players

    def plass(self):
        pass
