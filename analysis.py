import pandas as pd
import numpy as np
import os
import scipy.stats as stats
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
            download: boolean, default false, whether to save the plot to the data/processed folder
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
            download: boolean, default false, whether to save the plot to the data/processed folder
    Returns:
        df: pd.DataFrame, normalized fantasy points by season in career, with rows as players, 
          columns as season in career (1 is rookie year), entries as fantasy points in that season
    """
    fp_age = age_df.copy()
    #Normalize the fantasy points by scaling them to the player's best season
    fp_age = normalized_fantasy_points_by_age(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    #Unstack the dataframe to get row entries of player name, age, fantasy oints
    fp_age = fp_age.unstack().to_frame().reset_index(drop = False)
    fp_age.columns = ['Age', 'Player Name', 'Fantasy Points']
    #Drop rows where no fantasy points present
    fp_age = fp_age[fp_age['Fantasy Points'].notnull()].reset_index(drop = True)
    fp_age['Age'] = fp_age['Age'].astype(int)
    #Get the career year by taking each player's minimum age in the dataset and subtracting that (min_age - 1) from their age
    fp_age['Career Year'] = fp_age['Age'] - (fp_age.groupby('Player Name')['Age'].transform(np.min) - 1)
    fp_age = fp_age[['Player Name', 'Career Year', 'Fantasy Points']]
    #Pivot the table back to get the columns as the career year, index as player name, entries as fantasy points
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
            download: boolean, default false, whether to save the plot to the data/processed folder
    Returns:
        df: pd.Series, median fantasy points by age
    """
    fp_age = age_df.copy()
    #Get the normalized fantasy points by age
    fp_age = normalized_fantasy_points_by_age(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    #Calculate the median of each age
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
            download: boolean, default false, whether to save the plot to the data/processed folder
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
            download: boolean, default false, whether to save the plot to the data/processed folder
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
            download: boolean, default false, whether to save the plot to the data/processed folder
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


def paired_t_test_by_age(age_df, *, min_years = 0, fp_cutoff_flat = 0):
    """
        Get a table of paired t-test p-values by age jump
        Arguments:
            age_df: pd.DataFrame, fantasy points by age
        keyword:
            min_years: int, minimum number of years played
            fp_cutoff_flat: float, minimum fantasy points to have hit in a year
        Returns:
            p_values: pd.DataFrame, paired t-test p-values by age jumps
    """
    fp_age = age_df.copy()
    fp_age = normalized_fantasy_points_by_age(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    p_values = pd.Series()
    for i in range(len(fp_age.columns) - 1):
        #Create the column name to show the age comparison/jump (e.g. 23-24)
        col_name = str(fp_age.columns[i]) + '-' + str(fp_age.columns[i + 1])
        #Get players who have entries at both ages for comparison
        temp_df = fp_age[fp_age[fp_age.columns[i]].notnull() & fp_age[fp_age.columns[i + 1]].notnull()]
        #Need at least two values in sample to calculate paired t-test
        if len(temp_df) <= 1:
            continue
        #Calculate paired t-test p-value
        p_values[col_name] = stats.ttest_rel(temp_df[fp_age.columns[i]], temp_df[fp_age.columns[i + 1]], alternative = 'greater')[1]
    return p_values


def paired_t_test_by_career_season(age_df, *, min_years = 0, fp_cutoff_flat = 0):
    """
        Get a table of paired t-test p-values by career season jumps
        Arguments:
            age_df: pd.DataFrame, fantasy points by age
            keyword:
                min_years: int, minimum number of years played
                fp_cutoff_flat: float, minimum fantasy points to have hit in a year
        Returns:
            p_values: pd.DataFrame, paired t-test p-values by age jumps
    """
    fp_age = age_df.copy()
    fp_age = normalized_fantasy_points_by_career_season(fp_age, min_years = min_years, fp_cutoff_flat = fp_cutoff_flat)
    p_values = pd.Series()
    for i in range(len(fp_age.columns) - 1):
        #Create the column name to show the career season comparison/jump (e.g. 3-4)
        col_name = str(fp_age.columns[i]) + '-' + str(fp_age.columns[i + 1])
        #Get players who have entries at both career seasons for comparison
        temp_df = fp_age[fp_age[fp_age.columns[i]].notnull() & fp_age[fp_age.columns[i + 1]].notnull()]
        #Need at least two values in sample to calculate paired t-test
        if len(temp_df) <= 1:
            continue
        #Calculate paired t-test p-value
        p_values[col_name] = stats.ttest_rel(temp_df[temp_df.columns[i]], temp_df[temp_df.columns[i + 1]], alternative = 'greater')[1]
    return p_values


def paired_t_test_by_age_and_position(qb_age_df, rb_age_df, wr_age_df, te_age_df, *, min_years_dict = {}, fp_cutoff_flat_dict = {}, download = False):
    """
        Get a table of paired t-test p-values by age jump, where each row is a position
        Arguments:
            qb_age_df: pd.DataFrame, fantasy points by age for QBs
            rb_age_df: pd.DataFrame, fantasy points by age for RBs
            wr_age_df: pd.DataFrame, fantasy points by age for WRs
            te_age_df: pd.DataFrame, fantasy points by age for TEs
            keyword:
                min_years_dict: dictionary, minimum number of years played by position, e.g. ['QB' : 3, 'RB' : 5]. Default is 0 for all positions
                fp_cutoff_flat_dict: dictionary, minimum number of years played by position, e.g. ['QB' : 75, 'RB' : 45]. Default is 0 for all positions
                download: boolean, default false, whether to save the plot to the data/processed folder
        Returns:
            p_values: pd.DataFrame, paired t-test p-values by age jumps, with each row as a position
    """
    #Perform the paired t_tests for each position
    qb_p_values = paired_t_test_by_age(qb_age_df, min_years = min_years_dict.get('QB', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('QB', 0))
    rb_p_values = paired_t_test_by_age(rb_age_df, min_years = min_years_dict.get('RB', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('RB', 0))
    wr_p_values = paired_t_test_by_age(wr_age_df, min_years = min_years_dict.get('WR', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('WR', 0))
    te_p_values = paired_t_test_by_age(te_age_df, min_years = min_years_dict.get('TE', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('TE', 0))
    #Name each of the resulting series
    qb_p_values.name = 'QB'
    rb_p_values.name = 'RB'
    wr_p_values.name = 'WR'
    te_p_values.name = 'TE'
    #Concatenate the series into a dataframe
    p_values = pd.concat([qb_p_values, rb_p_values, wr_p_values, te_p_values], axis = 1)
    #Transpose the dataframe to make the rows positions and drop null columns
    p_values = p_values.T
    p_values = p_values.dropna(axis = 1, how = 'all')
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        p_values.to_csv(os.path.abspath('../data/processed/p_values_by_age.csv'))
    return p_values

def paired_t_test_by_career_season_and_position(qb_age_df, rb_age_df, wr_age_df, te_age_df, *, min_years_dict = {}, fp_cutoff_flat_dict = {}, download = False):
    """
        Get a table of paired t-test p-values by age jump, where each row is a position
        Arguments:
            qb_age_df: pd.DataFrame, fantasy points by age for QBs
            rb_age_df: pd.DataFrame, fantasy points by age for RBs
            wr_age_df: pd.DataFrame, fantasy points by age for WRs
            te_age_df: pd.DataFrame, fantasy points by age for TEs
            keyword:
                min_years_dict: dictionary, minimum number of years played by position, e.g. ['QB' : 3, 'RB' : 5]. Default is 0 for all positions
                fp_cutoff_flat_dict: dictionary, minimum number of years played by position, e.g. ['QB' : 75, 'RB' : 45]. Default is 0 for all positions
                download: boolean, default false, whether to save the plot to the data/processed folder
        Returns:
            p_values: pd.DataFrame, paired t-test p-values by age jumps, with each row as a position
    """
    #Perform the paired t_tests for each position
    qb_p_values = paired_t_test_by_career_season(qb_age_df, min_years = min_years_dict.get('QB', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('QB', 0))
    rb_p_values = paired_t_test_by_career_season(rb_age_df, min_years = min_years_dict.get('RB', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('RB', 0))
    wr_p_values = paired_t_test_by_career_season(wr_age_df, min_years = min_years_dict.get('WR', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('WR', 0))
    te_p_values = paired_t_test_by_career_season(te_age_df, min_years = min_years_dict.get('TE', 0), fp_cutoff_flat = fp_cutoff_flat_dict.get('TE', 0))
    #Name each of the resulting series
    qb_p_values.name = 'QB'
    rb_p_values.name = 'RB'
    wr_p_values.name = 'WR'
    te_p_values.name = 'TE'
    #Concatenate the series into a dataframe
    p_values = pd.concat([qb_p_values, rb_p_values, wr_p_values, te_p_values], axis = 1)
    #Transpose the dataframe to make the rows positions and drop null columns
    p_values = p_values.T
    p_values = p_values.dropna(axis = 1, how = 'all')
    if download:
        if not os.path.exists(os.path.abspath('../data/')):
            Logger.debug('Making data folder')
            os.mkdir(os.path.abspath('../data'))
        if not os.path.exists(os.path.abspath('../data/processed/')):
            Logger.debug('Making processed data folder')
            os.mkdir(os.path.abspath('../data/processed'))
        p_values.to_csv(os.path.abspath('../data/processed/p_values_by_career_season.csv'))
    return p_values
