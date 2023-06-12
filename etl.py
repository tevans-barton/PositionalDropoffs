import json
import pandas as pd
import numpy as np
import os
import sys
import time
sys.path.append('/Users/tevans-barton/AAASideProjects/')
from pfr_scraping import pfr_scraping
package_directory = os.path.dirname(os.path.abspath(__file__))

import logging
logging.basicConfig(filename='../logger.log', format='%(asctime)s %(levelname)s:%(name)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)
Logger = logging.getLogger(__name__)

def get_fantasy_points_by_age(position):
    """
    Get fantasy points by age for a given position
    Arguments:
        position: string, two letter position abbreviation to get fantasy points by age for
    Returns:
        df: pandas dataframe, fantasy points by age for a given position
    """
    Logger.debug('Running get_fantasy_points_by_age for {p}'.format(p = position))
    #Open the .csv file if it already exists
    if os.path.exists(os.path.abspath('../data/raw/{pos}_age_fantasy_points.csv'.format(pos = position))):
        Logger.debug('Reading in {pos}_age_fantasy_points.csv'.format(pos = position))
        df = pd.read_csv(os.path.abspath('../data/raw/{pos}_age_fantasy_points.csv'.format(pos = position)), index_col = 0)
        return df
    with open(package_directory + '/data-params.json') as fh:
        data_cfg = json.load(fh)
    years = data_cfg['years']
    player_slugs = {}
    for y in years:
        player_slugs.update(pfr_scraping.get_all_players_slugs(y, position))
        time.sleep(10)
    #Get the players names from the keys of the slug dictionary
    players = list(player_slugs.keys())
    #Sort the players by last name
    players.sort(key = lambda x : x.split()[1])
    age_df = pd.DataFrame()
    for player in players:
        time.sleep(6)
        Logger.debug('READING IN {p}'.format(p = player))
        stats = pfr_scraping.get_player_career_stats_from_slug(player_slugs[player])
        fantasy_points = stats.set_index('Age')['*Fantasy Points*']
        fantasy_points.name = player
        age_df = pd.merge(age_df, fantasy_points, how = 'outer', left_index = True, right_index = True)
    if not os.path.exists(os.path.abspath('../data/')):
        Logger.debug('Making data folder')
        os.mkdir(os.path.abspath('../data'))
    if not os.path.exists(os.path.abspath('../data/raw/')):
        Logger.debug('Making raw data folder')
        os.mkdir(os.path.abspath('../data/raw'))
    age_df.T.to_csv(os.path.abspath('../data/raw/{pos}_age_fantasy_points.csv'.format(pos = position)))
    return age_df.T

def get_fantasy_points_by_carries():
    """
    Get fantasy points by carries for running backs
    Arguments:
        None
    Returns:
        df: pandas dataframe, fantasy points by carries for running backs
    """
    Logger.debug('Running get_fantasy_points_by_carries')
    #Open the .csv file if it already exists
    if os.path.exists(os.path.abspath('../data/raw/RB_carries_fantasy_points.csv')):
        Logger.debug('Reading in rb_carries_fantasy_points.csv')
        df = pd.read_csv(os.path.abspath('../data/raw/RB_carries_fantasy_points.csv'), index_col = 0)
        return df
    with open(package_directory + '/data-params.json') as fh:
        data_cfg = json.load(fh)
    years = data_cfg['years']
    player_slugs = {}
    for y in years:
        player_slugs.update(pfr_scraping.get_all_players_slugs(y, 'RB'))
        time.sleep(10)
    #Get the players names from the keys of the slug dictionary
    players = list(player_slugs.keys())
    #Sort the players by last name
    players.sort(key = lambda x : x.split()[1])
    carries_df = pd.DataFrame()
    for player in players:
        time.sleep(6)
        Logger.debug('READING IN {p}'.format(p = player))
        stats = pfr_scraping.get_player_career_stats_from_slug(player_slugs[player])
        #Get the total number of carries the running back has had prior to the given season
        stats['Total Carries'] = stats['Carries'].fillna(0).shift(1).cumsum()
        stats = stats[stats['Total Carries'].notnull()]
        stats['Player Name'] = [player] * len(stats)
        fantasy_points = stats.reset_index(drop = False)[['Player Name', 'Year', 'Total Carries', '*Fantasy Points*']]
        carries_df = pd.concat([carries_df, fantasy_points], axis = 0, ignore_index = True)
    if not os.path.exists(os.path.abspath('../data/')):
        Logger.debug('Making data folder')
        os.mkdir(os.path.abspath('../data'))
    if not os.path.exists(os.path.abspath('../data/raw/')):
        Logger.debug('Making raw data folder')
        os.mkdir(os.path.abspath('../data/raw'))
    carries_df.to_csv(os.path.abspath('../data/raw/RB_carries_fantasy_points.csv'))
    return carries_df

def get_fantasy_points_by_offensive_snaps(position):
    """
    Get fantasy points by carries for running backs
    Arguments:
        position: string, two letter position abbreviation to get fantasy points by age for
    Returns:
        df: pandas dataframe, fantasy points by carries for running backs
    """
    Logger.debug('Running get_fantasy_points_by_carries')
    #Open the .csv file if it already exists
    if os.path.exists(os.path.abspath('../data/raw/rb_carries_fantasy_points.csv')):
        Logger.debug('Reading in rb_carries_fantasy_points.csv')
        df = pd.read_csv(os.path.abspath('../data/raw/{pos}_carries_fantasy_points.csv'.format(pos = position)), index_col = 0)
        return df
    with open(package_directory + '/data-params.json') as fh:
        data_cfg = json.load(fh)
    years = data_cfg['years']
    player_slugs = {}
    for y in years:
        player_slugs.update(pfr_scraping.get_all_players_slugs(y, 'RB'))
        time.sleep(10)
    #Get the players names from the keys of the slug dictionary
    players = list(player_slugs.keys())
    #Sort the players by last name
    players.sort(key = lambda x : x.split()[1])
    snaps_df = pd.DataFrame()
    for player in players:
        time.sleep(6)
        Logger.debug('READING IN {p}'.format(p = player))
        stats = pfr_scraping.get_player_career_stats_from_slug(player_slugs[player])
        stats['Total Snaps'] = stats['Off. Snaps Num'].fillna(0).shift(1).cumsum()
        stats = stats[stats['Total Snaps'].notnull()]
        stats['Player Name'] = [player] * len(stats)
        fantasy_points = stats.reset_index(drop = False)[['Player Name', 'Year', 'Total Snaps', '*Fantasy Points*']]
        snaps_df = pd.concat([snaps_df, fantasy_points], axis = 0)
    if not os.path.exists(os.path.abspath('../data/')):
        Logger.debug('Making data folder')
        os.mkdir(os.path.abspath('../data'))
    if not os.path.exists(os.path.abspath('../data/raw/')):
        Logger.debug('Making raw data folder')
        os.mkdir(os.path.abspath('../data/raw'))
    snaps_df.to_csv(os.path.abspath('../data/raw/{pos}_snaps_fantasy_points.csv'.format(pos = position)))
    return snaps_df
