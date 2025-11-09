from rich.table import Table

class PlayerTable():
    def __init__(self, players):
        self._players = players

    def create_table(self, nationality):
        table = Table(title=f"Season 2024-25 players from {nationality}")

        table.add_column("name", justify="right", style="cyan", no_wrap=True)
        table.add_column("teams", style="magenta")
        table.add_column("goals", justify="right", style="green")
        table.add_column("assists", justify="right", style="green")
        table.add_column("points", justify="right", style="green")
    
        for player in self._players:
            table.add_row(
                str(player.name),
                str(player.team),
                str(player.goals),
                str(player.assists),
                str(player.points)
            )
        
        return(table)