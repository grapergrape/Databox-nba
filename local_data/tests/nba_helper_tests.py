import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from nba_helper import StatsFetcher 

class TestStatsFetcher(unittest.TestCase):
    def setUp(self):
        self.player_id_patch = patch("nba_helper.StatsFetcher._get_player_id", return_value=12345)
        self.player_game_log_patch = patch("nba_helper.playergamelog.PlayerGameLog")

        self.MockGetPlayerId = self.player_id_patch.start()
        self.MockPlayerGameLog = self.player_game_log_patch.start()

        mock_df = pd.DataFrame([
            {
                "GAME_DATE": "2023-01-01",
                "PTS": 30,
                "REB": 10,
                "AST": 8,
                "MIN": 35,
                "FGM": 10,
                "FGA": 20,
                "FTA": 5,
                "MATCHUP": "LAC",
            }]
        )
        print(mock_df)

        mock_game_log = MagicMock()
        mock_game_log.get_data_frames.return_value = [mock_df]
        self.MockPlayerGameLog.return_value = mock_game_log

        self.stats_fetcher = StatsFetcher()

    def tearDown(self):
        self.player_id_patch.stop()
        self.player_game_log_patch.stop()

    def test_get_player_id(self,):
        player_id = self.stats_fetcher._get_player_id("Luka Doncic")
        self.assertEqual(player_id, 12345)

    def test_fetch_all_game_stats(self):
        df = self.stats_fetcher.fetch_all_game_stats()
        self.assertEqual(len(df), 7)
        self.assertEqual(df.iloc[0]["points"], 30)
        self.assertEqual(df.iloc[0]["rebounds"], 10)
        self.assertEqual(df.iloc[0]["assists"], 8)
        self.assertEqual(df.iloc[0]["fg_pct"], 0.5)
        self.assertAlmostEqual(df.iloc[0]["ts_pct"], 0.676, places=3)
        self.assertEqual(df.iloc[0]["opposing_team"], "LAC")

    def test_standardize_date_to_iso(self):
        df = pd.DataFrame({"date": ["JAN 01, 2023"]})
        df = self.stats_fetcher.standardize_date_to_iso(df)
        self.assertEqual(df.iloc[0]["date"], "2023-01-01")

    def test_lower_precision_floats(self):
        df = pd.DataFrame({"value": [0.123456789]})
        df = self.stats_fetcher.lower_precision_floats(df)
        self.assertEqual(df.iloc[0]["value"], 0.123)


if __name__ == "__main__":
    unittest.main()
