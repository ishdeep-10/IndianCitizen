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


def plot_shotmap_understat_team(df_shots,team,league,teamcolor,situation):
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

    ## OpenPlay
    df_openplay = df[df['situation'] == 'OpenPlay']
    total_shots_op = df_openplay.shape[0]
    total_goals_op = df_openplay[df_openplay['result'] == 'Goal'].shape[0]
    total_xG_op = df_openplay['xG'].sum()
    xG_per_shot_op = total_xG_op / total_shots_op

    top_5_op = df_openplay.groupby('player')['id'].count()
    top_5_shooters_op = top_5_op.sort_values(ascending=False).head(5)
    top_5_shooters_df_op = top_5_shooters_op.reset_index()
    top_5_shooters_df_op.columns = ['player', 'number_of_shots']

    ## FromCorner
    df_fromcorner = df[df['situation'] == 'FromCorner']
    total_shots_c = df_fromcorner.shape[0]
    total_goals_c = df_fromcorner[df_fromcorner['result'] == 'Goal'].shape[0]
    total_xG_c = df_fromcorner['xG'].sum()
    xG_per_shot_c = total_xG_c / total_shots_c

    top_5_fc = df_fromcorner.groupby('player')['id'].count()
    top_5_shooters_fc = top_5_fc.sort_values(ascending=False).head(5)
    top_5_shooters_df_fc = top_5_shooters_fc.reset_index()
    top_5_shooters_df_fc.columns = ['player', 'number_of_shots']

    ## SetPiece
    df_setpiece = df[df['situation'] == 'SetPiece']
    total_shots_sp = df_setpiece.shape[0]
    total_goals_sp = df_setpiece[df_setpiece['result'] == 'Goal'].shape[0]
    total_xG_sp = df_setpiece['xG'].sum()
    xG_per_shot_sp = total_xG_sp / total_shots_sp

    top_5_sp = df_setpiece.groupby('player')['id'].count()
    top_5_shooters_sp = top_5_sp.sort_values(ascending=False).head(5)
    top_5_shooters_df_sp = top_5_shooters_sp.reset_index()
    top_5_shooters_df_sp.columns = ['player', 'number_of_shots']

    ## DirectFreekick
    df_freekick = df[df['situation'] == 'DirectFreekick']
    total_shots_fk = df_freekick.shape[0]
    total_goals_fk = df_freekick[df_freekick['result'] == 'Goal'].shape[0]
    total_xG_fk = df_freekick['xG'].sum()
    xG_per_shot_fk = total_xG_fk / total_shots_fk

    top_5_fk = df_freekick.groupby('player')['id'].count()
    top_5_shooters_fk = top_5_fk.sort_values(ascending=False).head(5)
    top_5_shooters_df_fk = top_5_shooters_fk.reset_index()
    top_5_shooters_df_fk.columns = ['player', 'number_of_shots']

    ## Penalty
    df_penalty = df[df['situation'] == 'Penalty']
    total_shots_p = df_penalty.shape[0]
    total_goals_p = df_penalty[df_penalty['result'] == 'Goal'].shape[0]
    total_xG_p = df_penalty['xG'].sum()
    xG_per_shot_p = total_xG_p / total_shots_p

    top_5_p = df_penalty.groupby('player')['id'].count()
    top_5_shooters_p = top_5_p.sort_values(ascending=False).head(5)
    top_5_shooters_df_p = top_5_shooters_p.reset_index()
    top_5_shooters_df_p.columns = ['player', 'number_of_shots']
    
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

    if situation == "all":
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
    elif situation == "OpenPlay":
        for x in df_openplay.to_dict(orient='records'):
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
    elif situation == "FromCorner":
        for x in df_fromcorner.to_dict(orient='records'):
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
    elif situation == "SetPiece":
        for x in df_setpiece.to_dict(orient='records'):
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

    elif situation == "DirectFreekick":
        for x in df_freekick.to_dict(orient='records'):
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
    elif situation == "Penalty":
        for x in df_penalty.to_dict(orient='records'):
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

    if situation == 'OpenPlay':
        shots_text = total_shots_op
    elif situation == 'FromCorner':
        shots_text = total_shots_c
    elif situation == 'SetPiece':
        shots_text = total_shots_sp
    elif situation == 'DirectFreekick':
        shots_text = total_shots_fk
    elif situation == 'Penalty':
        shots_text = total_shots_p
    else:
        shots_text = total_shots
    
    ax3.text(
        x=0.25, 
        y=0, 
        s=f'{shots_text}', 
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

    if situation == 'OpenPlay':
        goals_text = total_goals_op
    elif situation == 'FromCorner':
        goals_text = total_goals_c
    elif situation == 'SetPiece':
        goals_text = total_goals_sp
    elif situation == 'DirectFreekick':
        goals_text = total_goals_fk
    elif situation == 'Penalty':
        goals_text = total_goals_p
    else:
        goals_text = total_goals
    ax3.text(
        x=0.38, 
        y=0, 
        s=f'{goals_text}', 
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

    if situation == 'OpenPlay':
        xG_text = total_xG_op
    elif situation == 'FromCorner':
        xG_text = total_xG_c
    elif situation == 'SetPiece':
        xG_text = total_xG_sp
    elif situation == 'DirectFreekick':
        xG_text = total_xG_fk
    elif situation == 'Penalty':
        xG_text = total_xG_p
    else:
        xG_text = total_xG
    ax3.text(
        x=0.53, 
        y=0, 
        s=f'{xG_text:.2f}', 
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

    if situation == 'OpenPlay':
        xG_per_shot_text = xG_per_shot_op
    elif situation == 'FromCorner':
        xG_per_shot_text = xG_per_shot_c
    elif situation == 'SetPiece':
        xG_per_shot_text = xG_per_shot_sp
    elif situation == 'DirectFreekick':
        xG_per_shot_text = xG_per_shot_fk
    elif situation == 'Penalty':
        xG_per_shot_text = xG_per_shot_p
    else:
        xG_per_shot_text = xG_per_shot
    
    ax3.text(
        x=0.63, 
        y=0, 
        s=f'{xG_per_shot_text:.2f}', 
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

    if situation == 'OpenPlay':
        for i, (player, shots) in enumerate(zip(top_5_shooters_df_op['player'], top_5_shooters_df_op['number_of_shots'])):
            y_pos = 1 - (i * 0.12)  # Adjust spacing between players
            ax4.text(0.5, y_pos, player.split()[-1], fontsize=15, fontproperties=font_prop, color='white', ha='center')
            ax4.text(0.5, y_pos - 0.05, f'{shots} shots', fontsize=12, fontproperties=font_prop, color=teamcolor, ha='center')
    elif situation == 'FromCorner':
        for i, (player, shots) in enumerate(zip(top_5_shooters_df_fc['player'], top_5_shooters_df_fc['number_of_shots'])):
            y_pos = 1 - (i * 0.12)  # Adjust spacing between players
            ax4.text(0.5, y_pos, player.split()[-1], fontsize=15, fontproperties=font_prop, color='white', ha='center')
            ax4.text(0.5, y_pos - 0.05, f'{shots} shots', fontsize=12, fontproperties=font_prop, color=teamcolor, ha='center')
    elif situation == 'SetPiece':
        for i, (player, shots) in enumerate(zip(top_5_shooters_df_sp['player'], top_5_shooters_df_sp['number_of_shots'])):
            y_pos = 1 - (i * 0.12)  # Adjust spacing between players
            ax4.text(0.5, y_pos, player.split()[-1], fontsize=15, fontproperties=font_prop, color='white', ha='center')
            ax4.text(0.5, y_pos - 0.05, f'{shots} shots', fontsize=12, fontproperties=font_prop, color=teamcolor, ha='center')
    elif situation == 'DirectFreekick':
        for i, (player, shots) in enumerate(zip(top_5_shooters_df_fk['player'], top_5_shooters_df_fk['number_of_shots'])):
            y_pos = 1 - (i * 0.12)  # Adjust spacing between players
            ax4.text(0.5, y_pos, player.split()[-1], fontsize=15, fontproperties=font_prop, color='white', ha='center')
            ax4.text(0.5, y_pos - 0.05, f'{shots} shots', fontsize=12, fontproperties=font_prop, color=teamcolor, ha='center')
    elif situation == 'Penalty':
        for i, (player, shots) in enumerate(zip(top_5_shooters_df_p['player'], top_5_shooters_df_p['number_of_shots'])):
            y_pos = 1 - (i * 0.12)  # Adjust spacing between players
            ax4.text(0.5, y_pos, player.split()[-1], fontsize=15, fontproperties=font_prop, color='white', ha='center')
            ax4.text(0.5, y_pos - 0.05, f'{shots} shots', fontsize=12, fontproperties=font_prop, color=teamcolor, ha='center')
    else:
        for i, (player, shots) in enumerate(zip(top_5_shooters_df['player'], top_5_shooters_df['number_of_shots'])):
            y_pos = 1 - (i * 0.12)  # Adjust spacing between players
            ax4.text(0.5, y_pos, player.split()[-1], fontsize=15, fontproperties=font_prop, color='white', ha='center')
            ax4.text(0.5, y_pos - 0.05, f'{shots} shots', fontsize=12, fontproperties=font_prop, color=teamcolor, ha='center')
    
    # Plot each player's name and their shot count
    
    
    ax4.set_axis_off()

    st.pyplot(fig)

def plot_shotmap_understat_player(df_shots,team,league,teamcolor,player,situation):
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

    ## OpenPlay
    df_openplay = df[df['situation'] == 'OpenPlay']
    total_shots_op = df_openplay.shape[0]
    total_goals_op = df_openplay[df_openplay['result'] == 'Goal'].shape[0]
    total_xG_op = df_openplay['xG'].sum()
    xG_per_shot_op = total_xG_op / total_shots_op

    ## FromCorner
    df_fromcorner = df[df['situation'] == 'FromCorner']
    total_shots_c = df_fromcorner.shape[0]
    total_goals_c = df_fromcorner[df_fromcorner['result'] == 'Goal'].shape[0]
    total_xG_c = df_fromcorner['xG'].sum()
    xG_per_shot_c = total_xG_c / total_shots_c

    ## SetPiece
    df_setpiece = df[df['situation'] == 'SetPiece']
    total_shots_sp = df_setpiece.shape[0]
    total_goals_sp = df_setpiece[df_setpiece['result'] == 'Goal'].shape[0]
    total_xG_sp = df_setpiece['xG'].sum()
    xG_per_shot_sp = total_xG_sp / total_shots_sp

    ## DirectFreekick
    df_freekick = df[df['situation'] == 'DirectFreekick']
    total_shots_fk = df_freekick.shape[0]
    total_goals_fk = df_freekick[df_freekick['result'] == 'Goal'].shape[0]
    total_xG_fk = df_freekick['xG'].sum()
    xG_per_shot_fk = total_xG_fk / total_shots_fk

    ## Penalty
    df_penalty = df[df['situation'] == 'Penalty']
    total_shots_p = df_penalty.shape[0]
    total_goals_p = df_penalty[df_penalty['result'] == 'Goal'].shape[0]
    total_xG_p = df_penalty['xG'].sum()
    xG_per_shot_p = total_xG_p / total_shots_p

    
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
    if situation == "all":
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
    elif situation == "OpenPlay":
        for x in df_openplay.to_dict(orient='records'):
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
    elif situation == "FromCorner":
        for x in df_fromcorner.to_dict(orient='records'):
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
    elif situation == "SetPiece":
        for x in df_setpiece.to_dict(orient='records'):
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

    elif situation == "DirectFreekick":
        for x in df_freekick.to_dict(orient='records'):
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
    elif situation == "Penalty":
        for x in df_penalty.to_dict(orient='records'):
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

    if situation == 'OpenPlay':
        shots_text = total_shots_op
    elif situation == 'FromCorner':
        shots_text = total_shots_c
    elif situation == 'SetPiece':
        shots_text = total_shots_sp
    elif situation == 'DirectFreekick':
        shots_text = total_shots_fk
    elif situation == 'Penalty':
        shots_text = total_shots_p
    else:
        shots_text = total_shots
    
    ax3.text(
        x=0.25, 
        y=0, 
        s=f'{shots_text}', 
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

    if situation == 'OpenPlay':
        goals_text = total_goals_op
    elif situation == 'FromCorner':
        goals_text = total_goals_c
    elif situation == 'SetPiece':
        goals_text = total_goals_sp
    elif situation == 'DirectFreekick':
        goals_text = total_goals_fk
    elif situation == 'Penalty':
        goals_text = total_goals_p
    else:
        goals_text = total_goals
    ax3.text(
        x=0.38, 
        y=0, 
        s=f'{goals_text}', 
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

    if situation == 'OpenPlay':
        xG_text = total_xG_op
    elif situation == 'FromCorner':
        xG_text = total_xG_c
    elif situation == 'SetPiece':
        xG_text = total_xG_sp
    elif situation == 'DirectFreekick':
        xG_text = total_xG_fk
    elif situation == 'Penalty':
        xG_text = total_xG_p
    else:
        xG_text = total_xG
    ax3.text(
        x=0.53, 
        y=0, 
        s=f'{xG_text:.2f}', 
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

    if situation == 'OpenPlay':
        xG_per_shot_text = xG_per_shot_op
    elif situation == 'FromCorner':
        xG_per_shot_text = xG_per_shot_c
    elif situation == 'SetPiece':
        xG_per_shot_text = xG_per_shot_sp
    elif situation == 'DirectFreekick':
        xG_per_shot_text = xG_per_shot_fk
    elif situation == 'Penalty':
        xG_per_shot_text = xG_per_shot_p
    else:
        xG_per_shot_text = xG_per_shot
    
    ax3.text(
        x=0.63, 
        y=0, 
        s=f'{xG_per_shot_text:.2f}', 
        fontsize=16, 
        fontproperties=font_prop, 
        color=teamcolor, 
        ha='left'
    )

    ax3.set_axis_off()
    st.pyplot(fig)

def plot_shotmap_understat_conceded(df,team,league,teamcolor,situation):
    df11 = df[((df['h_team'] == team) & (df['h_a'] == 'a')) & (df['result'] != 'OwnGoal')]
    df21 = df[((df['a_team'] == team) & (df['h_a'] == 'h')) & (df['result'] != 'OwnGoal')]
    df1 = pd.concat([df11, df21], ignore_index=True)

    df12 = df[((df['h_team'] == team) & (df['h_a'] == 'h')) & (df['result'] == 'OwnGoal')]
    df22 = df[((df['a_team'] == team) & (df['h_a'] == 'a')) & (df['result'] == 'OwnGoal')]
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

    ## OpenPlay
    df_openplay = df[df['situation'] == 'OpenPlay']
    total_shots_op = df_openplay.shape[0]
    total_goals_op = df_openplay[df_openplay['result'] == 'Goal'].shape[0]
    total_xG_op = df_openplay['xG'].sum()
    xG_per_shot_op = total_xG_op / total_shots_op

    ## FromCorner
    df_fromcorner = df[df['situation'] == 'FromCorner']
    total_shots_c = df_fromcorner.shape[0]
    total_goals_c = df_fromcorner[df_fromcorner['result'] == 'Goal'].shape[0]
    total_xG_c = df_fromcorner['xG'].sum()
    xG_per_shot_c = total_xG_c / total_shots_c

    ## SetPiece
    df_setpiece = df[df['situation'] == 'SetPiece']
    total_shots_sp = df_setpiece.shape[0]
    total_goals_sp = df_setpiece[df_setpiece['result'] == 'Goal'].shape[0]
    total_xG_sp = df_setpiece['xG'].sum()
    xG_per_shot_sp = total_xG_sp / total_shots_sp

    ## DirectFreekick
    df_freekick = df[df['situation'] == 'DirectFreekick']
    total_shots_fk = df_freekick.shape[0]
    total_goals_fk = df_freekick[df_freekick['result'] == 'Goal'].shape[0]
    total_xG_fk = df_freekick['xG'].sum()
    xG_per_shot_fk = total_xG_fk / total_shots_fk

    ## Penalty
    df_penalty = df[df['situation'] == 'Penalty']
    total_shots_p = df_penalty.shape[0]
    total_goals_p = df_penalty[df_penalty['result'] == 'Goal'].shape[0]
    total_xG_p = df_penalty['xG'].sum()
    xG_per_shot_p = total_xG_p / total_shots_p
    
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
        s=team, 
        fontsize=20, 
        fontproperties=font_prop, 
        fontweight='bold', 
        color=teamcolor, 
        ha='center'
    )
    ax1.text(
        x=0.5, 
        y=.7, 
        s=f'All shots conceded in the {league} 2024-25', 
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


    if situation == "all":
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
    elif situation == "OpenPlay":
        for x in df_openplay.to_dict(orient='records'):
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
    elif situation == "FromCorner":
        for x in df_fromcorner.to_dict(orient='records'):
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
    elif situation == "SetPiece":
        for x in df_setpiece.to_dict(orient='records'):
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

    elif situation == "DirectFreekick":
        for x in df_freekick.to_dict(orient='records'):
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
    elif situation == "Penalty":
        for x in df_penalty.to_dict(orient='records'):
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

    if situation == 'OpenPlay':
        shots_text = total_shots_op
    elif situation == 'FromCorner':
        shots_text = total_shots_c
    elif situation == 'SetPiece':
        shots_text = total_shots_sp
    elif situation == 'DirectFreekick':
        shots_text = total_shots_fk
    elif situation == 'Penalty':
        shots_text = total_shots_p
    else:
        shots_text = total_shots
    
    ax3.text(
        x=0.25, 
        y=0, 
        s=f'{shots_text}', 
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

    if situation == 'OpenPlay':
        goals_text = total_goals_op
    elif situation == 'FromCorner':
        goals_text = total_goals_c
    elif situation == 'SetPiece':
        goals_text = total_goals_sp
    elif situation == 'DirectFreekick':
        goals_text = total_goals_fk
    elif situation == 'Penalty':
        goals_text = total_goals_p
    else:
        goals_text = total_goals
    ax3.text(
        x=0.38, 
        y=0, 
        s=f'{goals_text}', 
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

    if situation == 'OpenPlay':
        xG_text = total_xG_op
    elif situation == 'FromCorner':
        xG_text = total_xG_c
    elif situation == 'SetPiece':
        xG_text = total_xG_sp
    elif situation == 'DirectFreekick':
        xG_text = total_xG_fk
    elif situation == 'Penalty':
        xG_text = total_xG_p
    else:
        xG_text = total_xG
    ax3.text(
        x=0.53, 
        y=0, 
        s=f'{xG_text:.2f}', 
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

    if situation == 'OpenPlay':
        xG_per_shot_text = xG_per_shot_op
    elif situation == 'FromCorner':
        xG_per_shot_text = xG_per_shot_c
    elif situation == 'SetPiece':
        xG_per_shot_text = xG_per_shot_sp
    elif situation == 'DirectFreekick':
        xG_per_shot_text = xG_per_shot_fk
    elif situation == 'Penalty':
        xG_per_shot_text = xG_per_shot_p
    else:
        xG_per_shot_text = xG_per_shot
    
    ax3.text(
        x=0.63, 
        y=0, 
        s=f'{xG_per_shot_text:.2f}', 
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
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/EPL/2024-25/shot_data.csv')
elif league == "La Liga":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/La_Liga/2024-25/shot_data.csv')
elif league == "Bundesliga":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/Bundesliga/2024-25/shot_data.csv')
elif league == "SerieA":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/Serie_A/2024-25/shot_data.csv')
elif league == "Ligue1":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Data/Ligue_1/2024-25/shot_data.csv')


team = st.selectbox('Select Team',df['h_team'].sort_values().unique(),index=0)
viz = st.selectbox('Select Viz Type',['Team ShotMap - Shots Attempted','Team ShotMap - Shots Conceded','Player ShotMap'],index=0)

number_of_colors = 1
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

if viz == 'Team ShotMap - Shots Attempted':
    situation = "all"
    # Create 5 columns for the buttons
    col1, col2, col3, col4, col5 = st.columns(5)

    # Add buttons in each column
    with col1:
        if st.button("OpenPlay"):
            situation = "OpenPlay"

    with col2:
        if st.button("FromCorner"):
            situation = "FromCorner"

    with col3:
        if st.button("SetPiece"):
            situation = "SetPiece"

    with col4:
        if st.button("DirectFreekick"):
            situation = "DirectFreekick"

    with col5:
        if st.button("Penalty"):
            situation = "Penalty"
    
    plot_shotmap_understat_team(df, team,league, color[0],situation)
elif viz == 'Team ShotMap - Shots Conceded':
    situation = "all"
    # Create 5 columns for the buttons
    col1, col2, col3, col4, col5 = st.columns(5)

    # Add buttons in each column
    with col1:
        if st.button("OpenPlay"):
            situation = "OpenPlay"

    with col2:
        if st.button("FromCorner"):
            situation = "FromCorner"

    with col3:
        if st.button("SetPiece"):
            situation = "SetPiece"

    with col4:
        if st.button("DirectFreekick"):
            situation = "DirectFreekick"

    with col5:
        if st.button("Penalty"):
            situation = "Penalty"
    plot_shotmap_understat_conceded(df, team,league, color[0],situation)
    
elif viz == 'Player ShotMap':
    df1 = df[(df['h_team'] == team) & (df['h_a'] == 'h')]
    df2 = df[(df['a_team'] == team) & (df['h_a'] == 'a')]
    team_df = pd.concat([df1, df2], ignore_index=True) 
    player = st.selectbox('Select Player',team_df['player'].sort_values().unique(),index=0)
    situation = "all"
    # Create 5 columns for the buttons
    col1, col2, col3, col4, col5 = st.columns(5)

    # Add buttons in each column
    with col1:
        if st.button("OpenPlay"):
            situation = "OpenPlay"

    with col2:
        if st.button("FromCorner"):
            situation = "FromCorner"

    with col3:
        if st.button("SetPiece"):
            situation = "SetPiece"

    with col4:
        if st.button("DirectFreekick"):
            situation = "DirectFreekick"

    with col5:
        if st.button("Penalty"):
            situation = "Penalty"
    plot_shotmap_understat_player(df, team,league, color[0],player,situation)

