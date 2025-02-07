import os
import requests
import logging

import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GitHubFetcher:
    """
    Class that handles github data fetching and processing.
    """
    def __init__(self):
        """
        Method to initialize the GitHubFetcher class with the necessary credentials and github repo attributes.
        """
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_owner = 'grapergrape' 
        self.repo_name = 'Databox-nba'
        self.api_url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits'
        self.headers = {
            'Authorization': f'token {self.github_token}'
        }

    def fetch_data(self) -> list:
        """
        Method to fetch all commits for the given repository.

        Parameters
        ----------
        None

        Returns
        -------

        List of commit dates. Same date can appear multiple times which indicates multiple commits on that day.
        """
        logging.info(f"Fetching all commits for {self.repo_name} repository.")
        commit_dates = []
        response = requests.get(self.api_url, headers=self.headers)
        commits = response.json()
        logging.info(f"Received {len(commits)} commits.")
        while commits:
            for commit in commits:
                commit_date = commit['commit']['author']['date']
                commit_dates.append(commit_date[:10])

            if 'next' in response.links:
                response = requests.get(response.links['next']['url'], headers=self.headers)
                commits = response.json()
            else:
                break
        return commit_dates

    def create_dataframe(self, commit_dates: list) -> pd.DataFrame:
        """
        Method that acts as a counter for the same commit dates and creates a pandas DataFrame.

        Parameters
        ----------
        commit_dates : list
            List of commit dates. Same date can appear multiple times which indicates multiple commits on that day.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: date, count, repository.
        """
        logging.info("Creating DataFrame with commit dates.")
        df = pd.DataFrame(commit_dates, columns=['date'])
        df['count'] = 1
        df = df.groupby('date').count().reset_index()
        df['repository'] = self.repo_name
        return df
    
    def fetch_all_commits(self) -> pd.DataFrame:
        """
        Main run method for this class.

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: date, count, repository.

        """
        commit_dates = self.fetch_data()
        df = self.create_dataframe(commit_dates)
        return df

if __name__ == '__main__':
    analyzer = GitHubFetcher('grapergrape', 'Databox-nba')
    commit_dates = analyzer.fetch_data()
    df = analyzer.create_dataframe(commit_dates)
    print(df)
