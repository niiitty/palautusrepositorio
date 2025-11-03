import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_player(self):
      player = self.stats.search("Semenko")

      self.assertIsNotNone(player)
      self.assertEqual(player.name, "Semenko")
      self.assertEqual(player.team, "EDM")
      self.assertEqual(player.goals, 4)
      self.assertEqual(player.assists, 12)

    def test_seach_missing_player(self):
        player = self.stats.search("Mallikas")
        self.assertIsNone(player)

    def test_filter_team(self):
      team = self.stats.team("EDM")
      self.assertEqual(len(team), 3)
      names = [p.name for p in team]
      self.assertCountEqual(names, ["Semenko", "Kurri", "Gretzky"])
    
    def test_top_players(self):
      top = self.stats.top(2)
      self.assertEqual(len(top), 3)
      names = [p.name for p in top]
      print(names)
      self.assertCountEqual(names, ["Yzerman", "Lemieux", "Gretzky"])
