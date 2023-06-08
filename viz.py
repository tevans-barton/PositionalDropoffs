import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sys
sys.path.append('/Users/tevans-barton/AAASideProjects/')
package_directory = os.path.dirname(os.path.abspath(__file__))

import logging
logging.basicConfig(filename='../logger.log', format='%(asctime)s %(levelname)s:%(name)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)
Logger = logging.getLogger(__name__)

plt.style.use('ggplot')

def plot_median_fantasy_points_age(age_median_series, position, download = False):
    """
    Plot the median fantasy points by age for a given position
    Arguments:
        age_df: pd.Series, median fantasy points by age for a given position
        position: string, position to label the visualization as
        download: boolean, default false, whether to save the plot to the visualizations folder
    Returns:
        None
    """
    age_median_series.plot(kind = 'bar', color='navy', figsize = (12, 8))
    plt.title('Median Fantasy Points by Age for {pos}'.format(pos = position), fontsize = 20)
    plt.ylabel('Individually Scaled Fantasy Points')
    plt.xlabel('Age')
    if download:
        if not os.path.exists(os.path.abspath('../visualizations/')):
            Logger.debug('Making visualizations folder')
            os.mkdir(os.path.abspath('../visualizations'))
        plt.savefig(os.path.abspath('../visualizations/{pos}_median_fantasy_points_age.png'.format(pos = position.replace(' ', '_'))))
    plt.show()

def plot_median_fantasy_points_career_season(age_median_series, position, download = False):
    """
    Plot the median fantasy points by age for a given position
    Arguments:
        age_df: pd.Series, median fantasy points by age for a given position
        position: string, position to label the visualization as
        download: boolean, default false, whether to save the plot to the visualizations folder
    Returns:
        None
    """
    plt.figure(figsize = (12, 8))
    age_median_series.plot(kind = 'bar', color='navy')
    plt.title('Median Fantasy Points by Season in Career for {pos}'.format(pos = position), fontsize = 20)
    plt.ylabel('Individually Scaled Fantasy Points')
    plt.xlabel('Age')
    if download:
        if not os.path.exists(os.path.abspath('../visualizations/')):
            Logger.debug('Making visualizations folder')
            os.mkdir(os.path.abspath('../visualizations'))
        plt.savefig(os.path.abspath('../visualizations/{pos}_median_fantasy_points_career_season.png'.format(pos = position.replace(' ', '_'))))
    plt.show()

def plot_box_and_whiskers_age(unstacked_age_fp, position, download = False):
    """
    Plot the box and whiskers plots by ages for a given position
    Arguments:
        unstacked_age_fp: pd.DataFrame, unstacked fantasy points by age for a given position
        position: string, position to label the visualization as
        download: boolean, default false, whether to save the plot to the visualizations folder
    Returns:
        None
    """
    plt.figure(figsize = (20, 12))
    #Plot the heatmap
    cmap = sns.diverging_palette(10, 133, as_cmap=True)
    median_map = unstacked_age_fp[['Age', 'Fantasy Points']].groupby('Age').median()['Fantasy Points']
    overall_median = unstacked_age_fp['Fantasy Points'].median()
    my_palette = {x: cmap(median_map[x] / (overall_median / .5)) for x in unstacked_age_fp['Age']}
    sns.boxplot(x = unstacked_age_fp['Age'], y = unstacked_age_fp['Fantasy Points'], linewidth = 2, palette = my_palette)
    plt.title('{pos} Fantasy Points by Age'.format(pos = position), fontsize = 24)
    plt.ylabel('Individually Scaled Fantasy Points', fontsize = 18)
    plt.xlabel('Age', fontsize = 18)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    if download:
        if not os.path.exists(os.path.abspath('../visualizations/')):
            Logger.debug('Making visualizations folder')
            os.mkdir(os.path.abspath('../visualizations'))
        plt.savefig(os.path.abspath('../visualizations/{pos}_box_and_whiskers_age.png'.format(pos = position.replace(' ', '_'))))
    plt.show()


def plot_box_and_whiskers_career_season(unstacked_career_season_fp, position, download = False):
    """
    Plot the box and whiskers plots by career season for a given position
    Arguments:
        unstacked_career_season_fp: pd.DataFrame, unstacked fantasy points by career season for a given position
        position: string, position to label the visualization as
        download: boolean, default false, whether to save the plot to the visualizations folder
    Returns:
        None
    """
    plt.figure(figsize = (20, 12))
    #Plot the heatmap
    cmap = sns.diverging_palette(10, 133, as_cmap=True)
    median_map = unstacked_career_season_fp[['Career Season', 'Fantasy Points']].groupby('Career Season').median()['Fantasy Points']
    overall_median = unstacked_career_season_fp['Fantasy Points'].median()
    my_palette = {x: cmap(median_map[x] / (overall_median / .5)) for x in unstacked_career_season_fp['Career Season']}
    sns.boxplot(x = unstacked_career_season_fp['Career Season'], y = unstacked_career_season_fp['Fantasy Points'], linewidth = 2, palette = my_palette)
    plt.title('{pos} Fantasy Points by Season in Career'.format(pos = position), fontsize = 24)
    plt.ylabel('Individually Scaled Fantasy Points', fontsize = 18)
    plt.xlabel('Career Season', fontsize = 18)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    if download:
        if not os.path.exists(os.path.abspath('../visualizations/')):
            Logger.debug('Making visualizations folder')
            os.mkdir(os.path.abspath('../visualizations'))
        plt.savefig(os.path.abspath('../visualizations/{pos}_box_and_whiskers_career_season.png'.format(pos = position.replace(' ', '_'))))
    plt.show()

def plot_heatmap_p_values_age_jumps(p_vals, download = False):
    """
    Plot the heatmap of p-values for age jumps
    Arguments:
        p_vals: pd.DataFrame, p-values for age jumps
        download: boolean, default false, whether to save the plot to the visualizations folder
    Returns:
        None
    """
    plt.figure(figsize = (20, 12))
    ax = sns.heatmap(p_vals.dropna(axis = 1, thresh = 2), cmap = sns.diverging_palette(10, 133, as_cmap=True), annot = True, fmt = '.5f', cbar=False, vmin=0, vmax=.13)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.xlabel('Age Jump', fontsize = 16, loc='center')
    plt.ylabel('Position', fontsize = 16)
    plt.yticks(rotation=0, fontsize = 14)
    plt.xticks(fontsize = 10)
    plt.title('P-Values for Paired T-Tests by Age Jump', fontsize = 20)
    if download:
        if not os.path.exists(os.path.abspath('../visualizations/')):
            Logger.debug('Making visualizations folder')
            os.mkdir(os.path.abspath('../visualizations'))
        plt.savefig(os.path.abspath('../visualizations/heatmap_p_values_age_jumps.png'))
    plt.show()

def plot_heatmap_p_values_career_season_jumps(p_vals, download = False):
    """
    Plot the heatmap of p-values for career season jumps
    Arguments:
        p_vals: pd.DataFrame, p-values for career season jumps
        download: boolean, default false, whether to save the plot to the visualizations folder
    Returns:
        None
    """
    plt.figure(figsize = (20, 12))
    ax = sns.heatmap(p_vals.dropna(axis = 1, thresh = 2), cmap = sns.diverging_palette(10, 133, as_cmap=True), annot = True, fmt = '.5f', cbar=False, vmin=0, vmax=.13)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.xlabel('Career Season Jump', fontsize = 16, loc='center')
    plt.ylabel('Position', fontsize = 16)
    plt.yticks(rotation=0, fontsize = 14)
    plt.xticks(fontsize = 10)
    plt.title('P-Values for Paired T-Tests by Career Season Jump', fontsize = 20)
    if download:
        if not os.path.exists(os.path.abspath('../visualizations/')):
            Logger.debug('Making visualizations folder')
            os.mkdir(os.path.abspath('../visualizations'))
        plt.savefig(os.path.abspath('../visualizations/heatmap_p_values_career_szn_jumps.png'))
    plt.show()