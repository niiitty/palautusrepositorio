from rich.console import Console
from player_reader import PlayerReader
from player_stats import PlayerStats
from player_table import PlayerTable


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    stats = PlayerStats(PlayerReader(url))

    nat_prompt = "/".join(sorted({p.nationality for p in stats.get_players()}))

    console = Console()

    while True:
        nationality = console.input(
            f"Nationality [magenta][{nat_prompt}][/magenta] (): ")
        if nationality == "":
            break

        table = PlayerTable(stats.top_scorers_by_nationality(nationality))
        console.print(table.create_table(nationality))


if __name__ == "__main__":
    main()
