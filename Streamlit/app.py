import random
import streamlit as st
import pandas as pd

from mplsoccer import VerticalPitch,Pitch
import matplotlib.font_manager as font_manager


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import matplotlib.font_manager as fm
from mplsoccer import FontManager
import matplotlib.image as mpimg
import matplotlib.patches as patches
import soccerdata as sd
from unidecode import unidecode

font_path = r'C:\Users\acer\Documents\GitHub\IndianCitizen\ScorePredict\Score Logos-20241022T100701Z-001\Score Logos\Sora_Font\Sora-Regular.ttf'
font_prop = fm.FontProperties(fname=font_path)
fm_sora = FontManager()

background='#0C0D0E'

def plot_shotmap_fotmob(df,team,teamcolor):
    total_shots = df.shape[0]
    total_goals = df[df['eventType'] == 'Goal'].shape[0]
    total_xG = df['expectedGoals'].sum()
    xG_per_shot = total_xG / total_shots
    points_average_distance = df['x'].mean()
    actual_average_distance = 120 - (df['x'] * 1.2).mean()
    
    pitch = VerticalPitch(
    pitch_type='uefa', 
    half=True, 
    pitch_color=background, 
    pad_bottom=.5, 
    line_color='white',
    linewidth=.5,
    axis=True, 
    label=True
    )

    # create a subplot with 2 rows and 1 column
    fig = plt.figure(figsize=(8, 12))
    fig.patch.set_facecolor(background)


    # Top row for the team names and score
    # [left, bottom, width, height]

    ax1 = fig.add_axes([0, 0.7, 1, .2])
    ax1.set_facecolor(background)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    ax1.text(
        x=0.5, 
        y=.85, 
        s=team, 
        fontsize=20, 
        fontproperties=font_props, 
        fontweight='bold', 
        color=teamcolor, 
        ha='center'
    )
    ax1.text(
        x=0.5, 
        y=.7, 
        s=f'All shots in the Premier League 2024-25', 
        fontsize=14,
        fontweight='bold',
        fontproperties=font_props, 
        color='white', 
        ha='center'
    )
    ax1.text(
        x=0.25, 
        y=0.5, 
        s=f'Low Quality Chance', 
        fontsize=12, 
        fontproperties=font_props, 
        color='white', 
        ha='center'
    )

    # add a scatter point between the two texts
    ax1.scatter(
        x=0.37, 
        y=0.53, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.42, 
        y=0.53, 
        s=200, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.48, 
        y=0.53, 
        s=300, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.54, 
        y=0.53, 
        s=400, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.6, 
        y=0.53, 
        s=500, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.75, 
        y=0.5, 
        s=f'High Quality Chance', 
        fontsize=12, 
        fontproperties=font_props, 
        color='white', 
        ha='center'
    )


    ax1.text(
        x=0.45, 
        y=0.27, 
        s=f'Goal', 
        fontsize=10, 
        fontproperties=font_props, 
        color='white', 
        ha='right'
    )
    ax1.scatter(
        x=0.47, 
        y=0.3, 
        s=100, 
        color=teamcolor, 
        edgecolor='white', 
        linewidth=.8,
        alpha=.7
    )


    ax1.scatter(
        x=0.53, 
        y=0.3, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.55, 
        y=0.27, 
        s=f'No Goal', 
        fontsize=10, 
        fontproperties=font_props, 
        color='white', 
        ha='left'
    )

    ax1.set_axis_off()


    ax2 = fig.add_axes([.05, 0.25, .9, .5])
    ax2.set_facecolor(background)

    pitch.draw(ax=ax2)

    
    # create a scatter plot at y 100 - average_distance
    ax2.scatter(
        x=60, 
        y=points_average_distance, 
        s=100, 
        color='white',  
        linewidth=.8
    )
    # create a line from the bottom of the pitch to the scatter point
    ax2.plot(
        [60, 60], 
        [105, points_average_distance], 
        color='white', 
        linewidth=2
    )

    # Add a text label for the average distance
    ax2.text(
        x=60, 
        y=points_average_distance - 4, 
        s=f'Average Distance\n{actual_average_distance:.1f} yards', 
        fontsize=10, 
        fontproperties=font_props, 
        color=teamcolor, 
        ha='center'
    )

    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x['x'], 
            x['y'], 
            s=400 * x['expectedGoals'], 
            color=teamcolor if x['eventType'] == 'Goal' else background, 
            ax=ax2,
            alpha=.7,
            linewidth=.8,
            edgecolor='white'
        )
        
    ax2.set_axis_off()
    
    # add another axis for the stats
    ax3 = fig.add_axes([0, .2, 1, .05])
    ax3.set_facecolor(background)
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)

    ax3.text(
        x=0.25, 
        y=.5, 
        s='Shots', 
        fontsize=20, 
        fontproperties=font_props, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.25, 
        y=0, 
        s=f'{total_shots}', 
        fontsize=16, 
        fontproperties=font_props, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=.5, 
        s='Goals', 
        fontsize=20, 
        fontproperties=font_props, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=0, 
        s=f'{total_goals}', 
        fontsize=16, 
        fontproperties=font_props, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=.5, 
        s='xG', 
        fontsize=20, 
        fontproperties=font_props, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=0, 
        s=f'{total_xG:.2f}', 
        fontsize=16, 
        fontproperties=font_props, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=.5, 
        s='xG/Shot', 
        fontsize=20, 
        fontproperties=font_props, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=0, 
        s=f'{xG_per_shot:.2f}', 
        fontsize=16, 
        fontproperties=font_props, 
        color=teamcolor, 
        ha='left'
    )

    ax3.set_axis_off()
    
    return fig


def plot_shotmap_understat_team(df_shots,team,league,teamcolor):
    df1 = df_shots[(df_shots['h_team'] == team) & (df_shots['h_a'] == 'h') & (df_shots['result'] != 'OwnGoal')]
    df2 = df_shots[(df_shots['a_team'] == team) & (df_shots['h_a'] == 'a') & (df_shots['result'] != 'OwnGoal')]
    df = pd.concat([df1, df2], ignore_index=True)
    df['X'] = (df['X'] / 100) * 105 * 100
    df['Y'] = (df['Y'] / 100) * 68 * 100
    total_shots = df.shape[0]
    total_goals = df[df['result'] == 'Goal'].shape[0]
    total_xG = df['xG'].sum()
    xG_per_shot = total_xG / total_shots
    points_average_distance = df['X'].mean()
    actual_average_distance = 105 - (df['X'] * 1.2).mean()

    top_5 = df.groupby('player')['id'].count()

    # Sort in descending order and get the top 5
    top_5_shooters = top_5.sort_values(ascending=False).head(5)
    top_5_shooters_df = top_5_shooters.reset_index()
    top_5_shooters_df.columns = ['player', 'number_of_shots']
    
    pitch = VerticalPitch(
    pitch_type='uefa', 
    half=True, 
    pitch_color=background, 
    pad_bottom=.5, 
    line_color='white',
    linewidth=.5,
    axis=True, 
    label=True
    )

    # create a subplot with 2 rows and 1 column
    fig = plt.figure(figsize=(9, 10))
    fig.patch.set_facecolor(background)

    # Top row for the team names and score
    # [left, bottom, width, height]

    ax1 = fig.add_axes([0, 0.7, 1, .2])
    ax1.set_facecolor(background)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    ax1.text(
        x=0.5, 
        y=.85, 
        s=team, 
        fontsize=25, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color=teamcolor, 
        ha='center'
    )
    ax1.text(
        x=0.5, 
        y=.7, 
        s=f'All shots in the {league} 2024-25', 
        fontsize=16,
        fontweight='bold',
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )
    ax1.text(
        x=0.25, 
        y=0.5, 
        s=f'Low Quality Chance', 
        fontsize=12, 
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )

    # add a scatter point between the two texts
    ax1.scatter(
        x=0.37, 
        y=0.53, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.42, 
        y=0.53, 
        s=200, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.48, 
        y=0.53, 
        s=300, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.54, 
        y=0.53, 
        s=400, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.6, 
        y=0.53, 
        s=500, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.75, 
        y=0.5, 
        s=f'High Quality Chance', 
        fontsize=12, 
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )


    ax1.text(
        x=0.45, 
        y=0.27, 
        s=f'Goal', 
        fontsize=15, 
        fontproperties=font_prop, 
        color='white', 
        ha='right'
    )
    ax1.scatter(
        x=0.47, 
        y=0.3, 
        s=100, 
        color=teamcolor, 
        edgecolor='white', 
        linewidth=.8,
        alpha=.7
    )


    ax1.scatter(
        x=0.53, 
        y=0.3, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.55, 
        y=0.27, 
        s=f'No Goal', 
        fontsize=15, 
        fontproperties=font_prop, 
        color='white', 
        ha='left'
    )

    ax1.set_axis_off()

    
    ax2 = fig.add_axes([.05, 0.25, .9, .5])
    ax2.set_facecolor(background)
    
    pitch.draw(ax=ax2)

    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x['X'], 
            x['Y'], 
            s=400 * x['xG'], 
            color=teamcolor if x['result'] == 'Goal' else background, 
            ax=ax2,
            alpha=.7,
            linewidth=.8,
            edgecolor='white'
        )
        
    ax2.set_axis_off()
    
    # add another axis for the stats
    ax3 = fig.add_axes([0, .2, 1, .05])
    ax3.set_facecolor(background)
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)

    ax3.text(
        x=0.25, 
        y=.5, 
        s='Shots', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.25, 
        y=0, 
        s=f'{total_shots}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=.5, 
        s='Goals', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=0, 
        s=f'{total_goals}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=.5, 
        s='xG', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=0, 
        s=f'{total_xG:.2f}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=.5, 
        s='xG/Shot', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=0, 
        s=f'{xG_per_shot:.2f}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.set_axis_off()

    ax4 = fig.add_axes([0.85, 0.1, 0.15, 0.5])  # Adjust position and size as needed
    ax4.set_facecolor(background)
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    
    # Plot each player's name and their shot count
    for i, (player, shots) in enumerate(zip(top_5_shooters_df['player'], top_5_shooters_df['number_of_shots'])):
        y_pos = 1 - (i * 0.12)  # Adjust spacing between players
        ax4.text(0.5, y_pos, player.split()[-1], fontsize=15, fontproperties=font_prop, color='white', ha='center')
        ax4.text(0.5, y_pos - 0.05, f'{shots} shots', fontsize=12, fontproperties=font_prop, color=teamcolor, ha='center')
    
    ax4.set_axis_off()

    st.pyplot(fig)

def plot_shotmap_understat_player(df_shots,team,league,teamcolor,player):
    df1 = df_shots[(df_shots['h_team'] == team) & (df_shots['h_a'] == 'h')]
    df2 = df_shots[(df_shots['a_team'] == team) & (df_shots['h_a'] == 'a')]
    teamdf = pd.concat([df1, df2], ignore_index=True)
    df = teamdf[teamdf['player'] == player]
    df['X'] = (df['X'] / 100) * 105 * 100
    df['Y'] = (df['Y'] / 100) * 68 * 100
    total_shots = df.shape[0]
    total_goals = df[df['result'] == 'Goal'].shape[0]
    total_xG = df['xG'].sum()
    xG_per_shot = total_xG / total_shots
    points_average_distance = df['X'].mean()
    actual_average_distance = 105 - (df['X'] * 1.2).mean()
    
    pitch = VerticalPitch(
    pitch_type='uefa', 
    half=True, 
    pitch_color=background, 
    pad_bottom=.5, 
    line_color='white',
    linewidth=.5,
    axis=True, 
    label=True
    )

    # create a subplot with 2 rows and 1 column
    fig = plt.figure(figsize=(10, 12))
    fig.patch.set_facecolor(background)


    # Top row for the team names and score
    # [left, bottom, width, height]

    ax1 = fig.add_axes([0, 0.7, 1, .2])
    ax1.set_facecolor(background)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    ax1.text(
        x=0.5, 
        y=.85, 
        s=player, 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color=teamcolor, 
        ha='center'
    )
    ax1.text(
        x=0.5, 
        y=.7, 
        s=f'All shots in the {league} 2024-25', 
        fontsize=14,
        fontweight='bold',
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )
    ax1.text(
        x=0.25, 
        y=0.5, 
        s=f'Low Quality Chance', 
        fontsize=12, 
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )

    # add a scatter point between the two texts
    ax1.scatter(
        x=0.37, 
        y=0.53, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.42, 
        y=0.53, 
        s=200, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.48, 
        y=0.53, 
        s=300, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.54, 
        y=0.53, 
        s=400, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.6, 
        y=0.53, 
        s=500, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.75, 
        y=0.5, 
        s=f'High Quality Chance', 
        fontsize=12, 
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )


    ax1.text(
        x=0.45, 
        y=0.27, 
        s=f'Goal', 
        fontsize=10, 
        fontproperties=font_prop, 
        color='white', 
        ha='right'
    )
    ax1.scatter(
        x=0.47, 
        y=0.3, 
        s=100, 
        color=teamcolor, 
        edgecolor='white', 
        linewidth=.8,
        alpha=.7
    )


    ax1.scatter(
        x=0.53, 
        y=0.3, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.55, 
        y=0.27, 
        s=f'No Goal', 
        fontsize=10, 
        fontproperties=font_prop, 
        color='white', 
        ha='left'
    )

    ax1.set_axis_off()

    
    ax2 = fig.add_axes([.05, 0.25, .9, .5])
    ax2.set_facecolor(background)
    
    pitch.draw(ax=ax2)

    
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x['X'], 
            x['Y'], 
            s=400 * x['xG'], 
            color=teamcolor if x['result'] == 'Goal' else background, 
            ax=ax2,
            alpha=.7,
            linewidth=.8,
            edgecolor='white'
        )
        
    ax2.set_axis_off()
    
    # add another axis for the stats
    ax3 = fig.add_axes([0, .2, 1, .05])
    ax3.set_facecolor(background)
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)

    ax3.text(
        x=0.25, 
        y=.5, 
        s='Shots', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.25, 
        y=0, 
        s=f'{total_shots}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=.5, 
        s='Goals', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=0, 
        s=f'{total_goals}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=.5, 
        s='xG', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=0, 
        s=f'{total_xG:.2f}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=.5, 
        s='xG/Shot', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=0, 
        s=f'{xG_per_shot:.2f}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.set_axis_off()
    st.pyplot(fig)

def plot_shotmap_conceded_understat(df_shots,team,league,teamcolor):
    df11 = df_shots[((df_shots['h_team'] == team) & (df_shots['h_a'] == 'a'))]
    df21 = df_shots[((df_shots['a_team'] == team) & (df_shots['h_a'] == 'h'))]
    df1 = pd.concat([df11, df21], ignore_index=True)

    df12 = df_shots[((df_shots['h_team'] == team) & (df_shots['h_a'] == 'h')) & (df_shots['result'] == 'OwnGoal')]
    df22 = df_shots[((df_shots['a_team'] == team) & (df_shots['h_a'] == 'a')) & (df_shots['result'] == 'OwnGoal')]
    df2 = pd.concat([df12, df22], ignore_index=True)

    df = pd.concat([df1, df2], ignore_index=True)
    df['X'] = (df['X'] / 100) * 105 * 100
    df['Y'] = (df['Y'] / 100) * 68 * 100
    total_shots = df.shape[0]
    total_goals = df[(df['result'] == 'Goal') | (df['result'] == 'OwnGoal')].shape[0]
    total_xG = df['xG'].sum()
    xG_per_shot = total_xG / total_shots
    points_average_distance = df['X'].mean()
    actual_average_distance = 105 - (df['X'] * 1.2).mean()
    
    pitch = VerticalPitch(
    pitch_type='uefa', 
    half=True, 
    pitch_color=background, 
    pad_bottom=.5, 
    line_color='white',
    linewidth=.5,
    axis=True, 
    label=True
    )

    # create a subplot with 2 rows and 1 column
    fig = plt.figure(figsize=(9, 10))
    fig.patch.set_facecolor(background)


    # Top row for the team names and score
    # [left, bottom, width, height]

    ax1 = fig.add_axes([0, 0.7, 1, .2])
    ax1.set_facecolor(background)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    ax1.text(
        x=0.5, 
        y=.85, 
        s=team, 
        fontsize=25, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color=teamcolor, 
        ha='center'
    )
    ax1.text(
        x=0.5, 
        y=.7, 
        s=f'All shots conceded in the {league} 2024-25', 
        fontsize=18,
        fontweight='bold',
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )
    ax1.text(
        x=0.25, 
        y=0.5, 
        s=f'Low Quality Chance', 
        fontsize=14, 
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )

    # add a scatter point between the two texts
    ax1.scatter(
        x=0.37, 
        y=0.53, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.42, 
        y=0.53, 
        s=200, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.48, 
        y=0.53, 
        s=300, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.54, 
        y=0.53, 
        s=400, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )
    ax1.scatter(
        x=0.6, 
        y=0.53, 
        s=500, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.75, 
        y=0.5, 
        s=f'High Quality Chance', 
        fontsize=14, 
        fontproperties=font_prop, 
        color='white', 
        ha='center'
    )


    ax1.text(
        x=0.45, 
        y=0.27, 
        s=f'Goal', 
        fontsize=14, 
        fontproperties=font_prop, 
        color='white', 
        ha='right'
    )
    ax1.scatter(
        x=0.47, 
        y=0.3, 
        s=100, 
        color=teamcolor, 
        edgecolor='white', 
        linewidth=.8,
        alpha=.7
    )


    ax1.scatter(
        x=0.53, 
        y=0.3, 
        s=100, 
        color=background, 
        edgecolor='white', 
        linewidth=.8
    )

    ax1.text(
        x=0.55, 
        y=0.27, 
        s=f'No Goal', 
        fontsize=14, 
        fontproperties=font_prop, 
        color='white', 
        ha='left'
    )

    ax1.set_axis_off()

    
    ax2 = fig.add_axes([.05, 0.25, .9, .5])
    ax2.set_facecolor(background)
    
    pitch.draw(ax=ax2)


    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x['X'], 
            x['Y'], 
            s=400 * x['xG'], 
            color=teamcolor if x['result'] == 'Goal' else background, 
            ax=ax2,
            alpha=.7,
            linewidth=.8,
            edgecolor='white'
        )
        
    ax2.set_axis_off()
    
    # add another axis for the stats
    ax3 = fig.add_axes([0, .2, 1, .05])
    ax3.set_facecolor(background)
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)

    ax3.text(
        x=0.25, 
        y=.5, 
        s='Shots', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.25, 
        y=0, 
        s=f'{total_shots}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=.5, 
        s='Goals', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.38, 
        y=0, 
        s=f'{total_goals}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=.5, 
        s='xG', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.53, 
        y=0, 
        s=f'{total_xG:.2f}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=.5, 
        s='xG/Shot', 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color='white', 
        ha='left'
    )

    ax3.text(
        x=0.63, 
        y=0, 
        s=f'{xG_per_shot:.2f}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.set_axis_off()

    st.pyplot(fig)


st.title("Indian Citizen")
st.subheader("Football Analytics App")


league = st.selectbox('Select League',['Premier League','La Liga','Bundesliga','SerieA','Ligue1'],index=0)

if league == "Premier League":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/PL/2024-25/shot_data.csv')
elif league == "La Liga":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/LaLiga/2024-25/shot_data.csv')
elif league == "Bundesliga":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/Bundesliga/2024-25/shot_data.csv')
elif league == "SerieA":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/SeriaA/2024-25/shot_data.csv')
elif league == "Ligue1":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/Ligue1/2024-25/shot_data.csv')


team = st.selectbox('Select Team',df['h_team'].sort_values().unique(),index=0)
viz = st.selectbox('Select Viz Type',['Team ShotMap','Player ShotMap'],index=0)

number_of_colors = 1
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

if viz == 'Team ShotMap':
    plot_shotmap_understat_team(df, team,league, color[0])
    plot_shotmap_conceded_understat(df, team,league, color[0])
elif viz == 'Player ShotMap':
    df1 = df[(df['h_team'] == team) & (df['h_a'] == 'h')]
    df2 = df[(df['a_team'] == team) & (df['h_a'] == 'a')]
    team_df = pd.concat([df1, df2], ignore_index=True) 
    player = st.selectbox('Select Player',team_df['player'].sort_values().unique(),index=0)
    plot_shotmap_understat_player(df, team,league, color[0],player)
