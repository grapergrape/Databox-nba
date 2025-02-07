import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from github_helper import GitHubFetcher

class TestGitHubFetcher(unittest.TestCase):
    def setUp(self):
        self.github_token_patch = patch("os.getenv", return_value="fake_token")
        self.requests_get_patch = patch("requests.get")

        self.MockGetEnv = self.github_token_patch.start()
        self.MockRequestsGet = self.requests_get_patch.start()

        self.github_fetcher = GitHubFetcher()

    def tearDown(self):
        self.github_token_patch.stop()
        self.requests_get_patch.stop()

    def test_fetch_data(self):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'commit': {'author': {'date': '2025-02-07T12:34:56Z'}}},
            {'commit': {'author': {'date': '2025-02-06T11:22:33Z'}}},
            {'commit': {'author': {'date': '2025-02-07T14:56:78Z'}}}
        ]
        mock_response.links = {}
        self.MockRequestsGet.return_value = mock_response

        commit_dates = self.github_fetcher.fetch_data()
        self.assertEqual(len(commit_dates), 3)
        self.assertEqual(commit_dates, ['2025-02-07', '2025-02-06', '2025-02-07'])

    def test_create_dataframe(self):
        commit_dates = ['2025-02-07', '2025-02-06', '2025-02-07']
        df = self.github_fetcher.create_dataframe(commit_dates)

        expected_df = pd.DataFrame({
            'date': ['2025-02-06', '2025-02-07'],
            'count': [1, 2],
            'repository': ['Databox-nba', 'Databox-nba']
        })

        pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)

    def test_fetch_all_commits(self):
        with patch.object(self.github_fetcher, 'fetch_data', return_value=['2025-02-07', '2025-02-06', '2025-02-07']):
            df = self.github_fetcher.fetch_all_commits()

            expected_df = pd.DataFrame({
                'date': ['2025-02-06', '2025-02-07'],
                'count': [1, 2],
                'repository': ['Databox-nba', 'Databox-nba']
            })

            pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)

if __name__ == "__main__":
    unittest.main()
