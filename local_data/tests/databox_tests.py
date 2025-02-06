import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from databox import ApiException

from nba_helper import StatsFetcher
from databox_connector import DataboxFeed  

class TestDataboxFeed(unittest.TestCase):

    @patch('databox.ApiClient')
    @patch('databox.DefaultApi')
    def setUp(self, MockDefaultApi, MockApiClient):
        os.environ['DATABOX_API'] = 'fake_api_token'
        self.mock_api_client = MockApiClient.return_value
        self.mock_api_instance = MockDefaultApi.return_value
        self.databox_feed = DataboxFeed()

    def test_init_raises_error_without_api_token(self):
        del os.environ['DATABOX_API']
        with self.assertRaises(ValueError):
            DataboxFeed()
        os.environ['DATABOX_API'] = 'fake_api_token'  # Reset for other tests

    def test_send_data_success(self):
        self.mock_api_instance.data_post.return_value = None
        data = {
            'date': ['2025-02-06'],
            'points': [25],
            'rebounds': [10],
            'assists': [5],
            'minutes': [35],
            'fg_pct': [0.5],
            'ts_pct': [0.6],
            'opposing_team': ['LAC'],
            'season': ['2025']
        }
        df = pd.DataFrame(data)
        self.databox_feed.send_data(df)
        self.mock_api_instance.data_post.assert_called_once()

    def test_send_data_api_exception(self):
        self.mock_api_instance.data_post.side_effect = ApiException("API Error")
        data = {
            'date': ['2025-02-06'],
            'points': [25],
            'rebounds': [10],
            'assists': [5],
            'minutes': [35],
            'fg_pct': [0.5],
            'ts_pct': [0.6],
            'opposing_team': ['LAC'],
            'season': ['2025']
        }
        df = pd.DataFrame(data)
        self.databox_feed.send_data(df)
        self.mock_api_instance.data_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()

