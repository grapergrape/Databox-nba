import os
import requests
import logging

import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GitHubFetcher:
    def __init__(self, repo_owner, repo_name):
        load_dotenv()
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
        self.headers = {
            'Authorization': f'token {self.github_token}'
        }

    def fetch_all_commits(self):
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

    def create_dataframe(self, commit_dates):
        logging.info("Creating DataFrame with commit dates.")
        df = pd.DataFrame(commit_dates, columns=['date'])
        df['count'] = 1
        df = df.groupby('date').count().reset_index()
        df['repository'] = self.repo_name
        return df

if __name__ == '__main__':
    analyzer = GitHubFetcher('grapergrape', 'Databox-nba')
    commit_dates = analyzer.fetch_all_commits()
    df = analyzer.create_dataframe(commit_dates)
    print(df)
