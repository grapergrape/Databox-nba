import logging

from databox_connector import DataboxFeed
from nba_helper import StatsFetcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    logging.info("Started data export to Databox.")
    stats_fetcher = StatsFetcher()
    luka_game_stats_df = stats_fetcher.fetch_all_game_stats()
    logging.info("Fetched all game stats for Luka Dončić.")
    databox_feed = DataboxFeed()
    databox_feed.send_data(luka_game_stats_df)
    logging.info("Data export to Databox completed.")
