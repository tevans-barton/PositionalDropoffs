import pandas as pd
import numpy as np
import os
import sys
package_directory = os.path.dirname(os.path.abspath(__file__))

import logging
logging.basicConfig(filename='../logger.log', format='%(asctime)s %(levelname)s:%(name)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)
Logger = logging.getLogger(__name__)

def normalized_fantasy_points_by_age(age_df, *, min_years = 0, fp_cutoff_flat = 0, download = False):
    """
    Create a dataframe of normalized fantasy points by age
    Arguments:
        age_df: pd.DataFrame, fantasy points by age
        keyword:
            min_years: int, minimum number of years played
            fp_cutoff_flat: float, minimum fantasy points to have hit in a year
    Returns:
        df: pd.DataFrame, normalized fantasy points by age, with rows as players, 
          columns as ages, entries as fantasy points in that season
    """
    fp_age = age_df.copy()
    initial_players = len(fp_age)
    #Get the players who have played a certain number of years
    fp_age = fp_age.dropna(axis = 0, thresh = min_years)
    Logger.debug("Cut off {n} players: did not play {m} seasons".format(n = initial_players - len(fp_age), m = min_years))
    players_left = len(fp_age)
    #Get the players who have hit a certain fantasy point threshold
    fp_age = fp_age[fp_age.max(axis = 1) > fp_cutoff_flat]
    Logger.debug("Cut off {n} players: did not hit {p} fantasy points".format(n = players_left - len(fp_age), p = fp_cutoff_flat))
    Logger.debug("Players Left: {n}".format(n = len(fp_age)))
    #Normalize the fantasy points by scaling them to the player's best season
    fp_age = fp_age.divide(fp_age.max(axis = 1), axis = 0)
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        fp_age.to_csv(os.path.abspath('../data/processed/normalized_fp_by_age_min_szn_{y}_fp_cutoff_{fp}.csv'.format(y = min_years, fp = fp_cutoff_flat)))
    return fp_age


def normalized_fantasy_points_by_career_season(age_df, *, min_years = 0, fp_cutoff_flat = 0, download = False):
    """
    Create a dataframe of normalized fantasy points by season in career (1 is rookie year)
    Arguments:
        age_df: pd.DataFrame, fantasy points by age
        keyword:
            min_years: int, minimum number of years played
            fp_cutoff_flat: float, minimum fantasy points to have hit in a year
    Returns:
        df: pd.DataFrame, normalized fantasy points by season in career, with rows as players, 
          columns as season in career (1 is rookie year), entries as fantasy points in that season
    """
    fp_age = age_df.copy()
    #Normalize the fantasy points by scaling them to the player's best season
    fp_age = normalized_fantasy_points_by_age(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    #Get the median fantasy points by age
    fp_age = fp_age.unstack().to_frame().reset_index(drop = False)
    fp_age.columns = ['Age', 'Player Name', 'Fantasy Points']
    fp_age = fp_age[fp_age['Fantasy Points'].notnull()].reset_index(drop = True)
    fp_age['Age'] = fp_age['Age'].astype(int)
    fp_age['Career Year'] = fp_age['Age'] - (fp_age.groupby('Player Name')['Age'].transform(np.min) - 1)
    fp_age = fp_age[['Player Name', 'Career Year', 'Fantasy Points']]
    fp_age = fp_age.pivot(index = 'Player Name', columns = 'Career Year', values = 'Fantasy Points')
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        fp_age.to_csv(os.path.abspath('../data/processed/normalized_fp_by_career_season_min_szn_{y}_fp_cutoff_{fp}.csv'.format(y = min_years, fp = fp_cutoff_flat)))
    return fp_age
    

def median_fantasy_points_by_age(age_df, *, min_years = 0, fp_cutoff_flat = 0, download = False):
    """
    Create the final series of median fantasy points by age
    Arguments:
        age_df: pd.DataFrame, fantasy points by age
        keyword:
            min_years: int, minimum number of years played
            fp_cutoff_flat: float, minimum fantasy points to have hit in a year
    Returns:
        df: pd.Series, median fantasy points by age
    """
    fp_age = age_df.copy()
    fp_age = normalized_fantasy_points_by_age(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    fp_age = fp_age.median(axis = 0).sort_index()
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        fp_age.to_csv(os.path.abspath('../data/processed/median_fp_by_age_min_szn_{y}_fp_cutoff_{fp}.csv'.format(y = min_years, fp = fp_cutoff_flat)))
    return fp_age


def median_fantasy_points_by_career_season(age_df, *, min_years = 0, fp_cutoff_flat = 0, download = False):
    """
    Create the final series of median fantasy points by season in career (1 is rookie year)
    Arguments:
        age_df: pd.DataFrame, fantasy points by age
        keyword:
            min_years: int, minimum number of years played
            fp_cutoff_flat: float, minimum fantasy points to have hit in a year
    Returns:
        df: pd.Series, median fantasy points by season in career (1 is rookie)
    """
    fp_age = age_df.copy()
    #Normalize the fantasy points by scaling them to the player's best season
    fp_age = normalized_fantasy_points_by_age(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    #Get the median fantasy points by age
    fp_age = fp_age.unstack().to_frame().reset_index(drop = False)
    fp_age.columns = ['Age', 'Player Name', 'Fantasy Points']
    fp_age = fp_age[fp_age['Fantasy Points'].notnull()].reset_index(drop = True)
    fp_age['Age'] = fp_age['Age'].astype(int)
    fp_age['Career Year'] = fp_age['Age'] - (fp_age.groupby('Player Name')['Age'].transform(np.min) - 1)
    fp_age = fp_age[['Player Name', 'Career Year', 'Fantasy Points']]
    fp_age = fp_age[['Career Year', 'Fantasy Points']].groupby('Career Year').median()['Fantasy Points'].sort_index()
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        fp_age.to_csv(os.path.abspath('../data/processed/median_fp_by_career_season_min_szn_{y}_fp_cutoff_{fp}.csv'.format(y = min_years, fp = fp_cutoff_flat)))
    return fp_age


def unstack_fantasy_points_and_age(age_df, *, min_years = 0, fp_cutoff_flat = 0, download = False):
    """
    Unstack the fantasy points by age dataframe
    Arguments:
        age_df: pd.DataFrame, fantasy points by age
        keyword:
            min_years: int, minimum number of years played
            fp_cutoff_flat: float, minimum fantasy points to have hit in a year
    Returns:
        fp_age: pd.DataFrame, fantasy points by age unstacked (Columns: Player Name, Age, Fantasy Points)
    """
    fp_age = age_df.copy()
    fp_age = normalized_fantasy_points_by_age(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    fp_age = fp_age.unstack().to_frame().reset_index(drop = False)
    fp_age.columns = ['Age', 'Player Name', 'Fantasy Points']
    fp_age = fp_age[fp_age['Fantasy Points'].notnull()].reset_index(drop = True)
    fp_age['Age'] = fp_age['Age'].astype(int)
    fp_age = fp_age[['Player Name', 'Age', 'Fantasy Points']]
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        fp_age.to_csv(os.path.abspath('../data/processed/unstacked_fp_by_age_min_szn_{y}_fp_cutoff_{fp}.csv'.format(y = min_years, fp = fp_cutoff_flat)))
    return fp_age


def unstack_fantasy_points_and_career_season(age_df, *, min_years = 0, fp_cutoff_flat = 0, download = False):
    """
    Unstack age dataframe to fantasy points by career season dataframe
    Arguments:
        age_df: pd.DataFrame, fantasy points by age
        keyword:
            min_years: int, minimum number of years played
            fp_cutoff_flat: float, minimum fantasy points to have hit in a year
    Returns:
        fp_age: pd.DataFrame, fantasy points by career season unstacked (Columns: Player Name, Career Season, Fantasy Points)
    """
    fp_age = age_df.copy()
    fp_age = normalized_fantasy_points_by_career_season(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    fp_age = fp_age.unstack().to_frame().reset_index(drop = False)
    fp_age.columns = ['Career Season', 'Player Name', 'Fantasy Points']
    fp_age = fp_age[fp_age['Fantasy Points'].notnull()].reset_index(drop = True)
    fp_age['Career Season'] = fp_age['Career Season'].astype(int)
    fp_age = fp_age[['Player Name', 'Career Season', 'Fantasy Points']]
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        fp_age.to_csv(os.path.abspath('../data/processed/unstacked_fp_by_career_season_min_szn_{y}_fp_cutoff_{fp}.csv'.format(y = min_years, fp = fp_cutoff_flat)))
    return fp_age

