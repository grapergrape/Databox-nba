import logging

from databox_connector import DataboxFeed
from nba_helper import StatsFetcher
from github_helper import GitHubFetcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    logging.info("Started data export to Databox.")
    stats_fetcher = StatsFetcher()
    luka_game_stats_df = stats_fetcher.fetch_all_game_stats()
    commti_fetcher = GitHubFetcher()
    my_commits_df = commti_fetcher.fetch_all_commits()

    logging.info("Fetched all game stats for Luka Dončić.")
    databox_feed = DataboxFeed()
    databox_feed.send_data_nba(luka_game_stats_df)
    databox_feed.send_data_github(my_commits_df)
    logging.info("Data export to Databox completed.")
