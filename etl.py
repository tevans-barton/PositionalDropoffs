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

