from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, All, Not, HasFewerThan

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)


    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all))


    #for player in stats.matches(matcher):
    #    print(player)


if __name__ == "__main__":
    main()
