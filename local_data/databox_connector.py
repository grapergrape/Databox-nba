import os
import pandas as pd
import logging

from dotenv import load_dotenv

import databox
from databox.rest import ApiException



load_dotenv()  # Load environment variables from a .env file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataboxFeed:
    """
    A class to feed data from a Pandas DataFrame to Databox using their API.

    Attributes
    ----------
    api_client : databox.ApiClient
        The API client for interacting with Databox.
    api_instance : databox.DefaultApi
        The default API instance for making requests to Databox.

    Methods
    -------
    send_data(df: pd.DataFrame) -> None:
        Sends data from a DataFrame to Databox.
    """

    def __init__(self):
        """
        Initializes the DataboxFeed class by setting up the API client with the token from environment variables.
        """
        api_token = os.getenv('DATABOX_API')
        if not api_token:
            raise ValueError("Databox API token is not set in the environment variables.")

        configuration = databox.Configuration(
            host="https://push.databox.com",
            username=api_token,
            password=""
        )

        # Initialize the API client with the correct headers
        self.api_client = databox.ApiClient(configuration, "Accept", "application/vnd.databox.v2+json")
        self.api_instance = databox.DefaultApi(self.api_client)

    def send_data_nba(self, df: pd.DataFrame) -> None:
        """
        Sends data from a DataFrame to Databox.

        Parameters
        ----------
        df : pd.DataFrame
            A DataFrame containing the data with columns: date, points, rebounds, assists, minutes, fg_pct, ts_pct, opposing_team, season.

        Raises
        ------
        ApiException
            If there is an error in sending data to Databox.
        Exception
            For any unexpected errors.
        """
        df = df.astype({
            'points': float,
            'rebounds': float,
            'assists': float,
            'minutes': float,
            'fg_pct': float,
            'ts_pct': float
        })
        for _, row in df.iterrows():
            data_dict = row.to_dict()
            push_data = [
                {
                    "key": "points",
                    "value": data_dict['points'],
                    "date": data_dict['date'],
                    "attributes": [
                        {"key": "opposing_team", "value": data_dict['opposing_team']},
                        {"key": "season", "value": data_dict['season']}
                    ]
                },
                {
                    "key": "rebounds",
                    "value": data_dict['rebounds'],
                    "date": data_dict['date'],
                    "attributes": [
                        {"key": "opposing_team", "value": data_dict['opposing_team']},
                        {"key": "season", "value": data_dict['season']}
                    ]
                },
                {
                    "key": "assists",
                    "value": data_dict['assists'],
                    "date": data_dict['date'],
                    "attributes": [
                        {"key": "opposing_team", "value": data_dict['opposing_team']},
                        {"key": "season", "value": data_dict['season']}
                    ]
                },
                {
                    "key": "minutes",
                    "value": data_dict['minutes'],
                    "date": data_dict['date'],
                    "attributes": [
                        {"key": "opposing_team", "value": data_dict['opposing_team']},
                        {"key": "season", "value": data_dict['season']}
                    ]
                },
                {
                    "key": "fg_pct",
                    "value": data_dict['fg_pct'],
                    "date": data_dict['date'],
                    "attributes": [
                        {"key": "opposing_team", "value": data_dict['opposing_team']},
                        {"key": "season", "value": data_dict['season']}
                    ]
                },
                {
                    "key": "ts_pct",
                    "value": data_dict['ts_pct'],
                    "date": data_dict['date'],
                    "attributes": [
                        {"key": "opposing_team", "value": data_dict['opposing_team']},
                        {"key": "season", "value": data_dict['season']}
                    ]
                }
            ]

            try:
                self.api_instance.data_post(push_data=push_data)
                logging.info(f"Successfully pushed data for date: {data_dict['date']}")
            except ApiException as e:
                logging.error(f"API Exception occurred: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")

    def send_data_github(self, df: pd.DataFrame) -> None:
        """
        Sends data from a DataFrame to Databox.

        Parameters
        ----------
        df : pd.DataFrame
            A DataFrame containing the data with columns: date, commits, additions, deletions, changed_files, repository.

        Raises
        ------
        ApiException
            If there is an error in sending data to Databox.
        Exception
            For any unexpected errors.
        """
        df = df.astype({
            'commits': float,
            'repository': str,
            'date': str
        })
        for _, row in df.iterrows():
            data_dict = row.to_dict()
            push_data = [
                {
                    "key": "commits",
                    "value": data_dict['commits'],
                    "date": data_dict['date'],
                    "attributes": [
                        {"key": "repository", "value": data_dict['repository']}
                    ]
                }
            ]
        
            try:
                self.api_instance.data_post(push_data=push_data)
                logging.info(f"Successfully pushed data for date: {data_dict['date']}")
            except ApiException as e:
                logging.error(f"API Exception occurred: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")