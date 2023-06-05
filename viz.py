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

def plot_box_and_whiskers_age(normalized_age_fp, position, download = False):
    """
    Plot the box and whiskers plots by ages for a given position
    Arguments:
        normalized_age_fp: pd.DataFrame, normalized fantasy points by age for a given position
        position: string, position to label the visualization as
        download: boolean, default false, whether to save the plot to the visualizations folder
    Returns:
        None
    """
    plt.figure(figsize = (20, 12))
    #Plot the heatmap
    cmap = sns.diverging_palette(10, 133, as_cmap=True)
    median_map = normalized_age_fp[['Age', 'Fantasy Points']].groupby('Age').median()['Fantasy Points']
    my_palette = {h: cmap(median_map[h]) for h in normalized_age_fp['Age']}
    ax = sns.boxplot(x = normalized_age_fp['Age'], y = normalized_age_fp['Fantasy Points'], linewidth = 2, palette = my_palette)
    plt.title('Plot of Fantasy Points by Age for {pos}'.format(pos = position), fontsize = 20)
    plt.ylabel('Individually Scaled Fantasy Points')
    plt.xlabel('Age')
    if download:
        if not os.path.exists(os.path.abspath('../visualizations/')):
            Logger.debug('Making visualizations folder')
            os.mkdir(os.path.abspath('../visualizations'))
        plt.savefig(os.path.abspath('../visualizations/{pos}_box_and_whiskers_age.png'.format(pos = position.replace(' ', '_'))))
    plt.show()

