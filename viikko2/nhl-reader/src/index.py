import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []
    nationality = input("Insert nationality: ")

    filtered_players = filter(lambda player: player["nationality"] == nationality, response)
    filtered_players = sorted(filtered_players, key=lambda player: player["goals"] + player["assists"], reverse=True)

    for player_dict in filtered_players:
      player = Player(player_dict)
      players.append(player)

    print(f"Players from {nationality}:")
    print()

    for player in players:
        print(player)

if __name__ == "__main__":
    main()