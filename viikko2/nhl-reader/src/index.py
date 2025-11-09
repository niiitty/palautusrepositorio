from player_reader import PlayerReader
from player_stats import PlayerStats
from player_table import PlayerTable
from rich.console import Console

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    nationalities = sorted({p.nationality for p in stats._players})
    nat_prompt = "/".join(nationalities)

    console = Console()

    while True:
        nationality = console.input(f"Nationality [magenta][{nat_prompt}][/magenta] (): ")
        if nationality == "":
            break

        players = stats.top_scorers_by_nationality(nationality)
        table = PlayerTable(players)
        console.print(table.create_table(nationality))


if __name__ == "__main__":
    main()