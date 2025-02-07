import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StatsFetcher:
    """
    A class to fetch and calculate game-by-game statistics for Luka Dončić.

    This class retrieves historical game data for Luka Dončić from his rookie season (2018-19) to the 2023-24 season
    and calculates relevant metrics such as FG% and TS%.

    Methods
    -------
    fetch_all_game_stats() -> pd.DataFrame:
        Fetches and returns a DataFrame with game-by-game stats for Luka Dončić.
    """

    def __init__(self):
        """
        Initializes the StatsFetcher class by identifying Luka Dončić and setting the seasons range.
        """
        self.player_id = self._get_player_id('Luka Doncic')
        self.seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']

    def _get_player_id(self, player_name: str) -> int:
        """
        Retrieves a player's ID using their full name.

        Parameters
        ----------
        player_name : str
            The full name of the player.
        
        Returns
        -------
        int
            The player's ID.
        """
        player = players.find_players_by_full_name(player_name)[0]
        return player['id']

    def _calculate_ts(self, pts: int, fga: int, fta: int) -> float:
        """
        Calculates the True Shooting Percentage (TS%) for given points, field goal attempts, and free throw attempts.

        Parameters
        ----------
        pts : int
            The total points scored.
        fga : int
            The total field goal attempts.
        fta : int   
            The total free throw attempts.

        Returns
        -------
        float
            The True Shooting Percentage (TS%).
        """
        return pts / (2 * (fga + 0.44 * fta)) if fga + 0.44 * fta > 0 else 0.0

    def fetch_all_game_stats(self) -> pd.DataFrame:
        """
        Fetches Luka Dončić's game stats for each game from 2018-19 to 2023-24.

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: date, points, rebounds, assists, minutes, fg_pct, ts_pct, opposing_team, season.
        """
        all_game_stats: List[pd.DataFrame] = []

        for season in self.seasons:
            logging.info(f"Fetching game stats for Luka Dončić for season {season}")
            game_logs = playergamelog.PlayerGameLog(player_id=self.player_id, season=season).get_data_frames()[0]
            game_logs['FG%'] = game_logs['FGM'] / game_logs['FGA']
            game_logs['TS%'] = game_logs.apply(lambda row: self._calculate_ts(row['PTS'], row['FGA'], row['FTA']), axis=1)
            game_logs['opposing_team'] = game_logs['MATCHUP'].apply(lambda x: x.split()[-1] if 'vs.' in x else x.split()[-1])
            game_logs['season'] = season

            game_logs = game_logs[['GAME_DATE', 'PTS', 'REB', 'AST', 'MIN', 'FG%', 'TS%', 'opposing_team', 'season']]
            game_logs.columns = ['date', 'points', 'rebounds', 'assists', 'minutes', 'fg_pct', 'ts_pct', 'opposing_team', 'season']

            all_game_stats.append(game_logs)

        combined_game_stats = pd.concat(all_game_stats, ignore_index=True)
        combined_game_stats = self.standardize_date_to_iso(combined_game_stats)
        combined_game_stats = self.lower_precision_floats(combined_game_stats)
        return combined_game_stats

    def standardize_date_to_iso(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes the date format in the DataFrame to ISO format (YYYY-MM-DD).
        Used because API returns non-standard date format: OCT 31, 2024 etc.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with a date column in non-standard format.

        Returns
        -------
        pd.DataFrame
            DataFrame with date column in ISO format.
        """
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        return df

    def lower_precision_floats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reduces the precision of float columns in the DataFrame to 3 decimal places.
        Databox supports up to 6 decimal places for float values.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with float columns.
        
        Returns
        -------
        pd.DataFrame
            DataFrame with float columns rounded to 3 decimal places
        """
        float_cols = df.select_dtypes(include=['float']).columns
        df[float_cols] = df[float_cols].round(3)
        return df
