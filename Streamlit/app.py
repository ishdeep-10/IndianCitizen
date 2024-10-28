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
font_props = fm.FontProperties(fname=font_path)
fm_sora = FontManager()

background='#0C0D0E'

def plot_shotmap(df,team,teamcolor):
    total_shots = df.shape[0]
    total_goals = df[df['eventType'] == 'Goal'].shape[0]
    total_xG = df['expectedGoals'].sum()
    xG_per_shot = total_xG / total_shots
    #points_average_distance = df['x'].mean()
    #actual_average_distance = 120 - (df['x'] * 1.2).mean()
    
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

    '''
    # create a scatter plot at y 100 - average_distance
    ax2.scatter(
        x=90, 
        y=points_average_distance, 
        s=100, 
        color='white',  
        linewidth=.8
    )
    # create a line from the bottom of the pitch to the scatter point
    ax2.plot(
        [90, 90], 
        [100, points_average_distance], 
        color='white', 
        linewidth=2
    )

    # Add a text label for the average distance
    ax2.text(
        x=90, 
        y=points_average_distance - 4, 
        s=f'Average Distance\n{actual_average_distance:.1f} yards', 
        fontsize=10, 
        fontproperties=font_props, 
        color=teamcolor, 
        ha='center'
    )
    '''

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


st.title("Indian Citizen")
st.subheader("Football Analytics App")


league = st.selectbox('Select League',['Premier League','La Liga','Bundesliga','SerieA','Ligue1','UCL'],index=0)

if league == "Premier League":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/StreamLit/Data/PL/2024-25/premier_league_2024-25_shot_data.csv')
elif league == "La Liga":
    df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/StreamLit/Data/LaLiga/2024-25/la_liga_2024-25_shot_data.csv')

team = st.selectbox('Select Team',df['teamName'].sort_values().unique(),index=0)
df_team = df[df['teamName'] == team]
teamcolor = df[df['teamName'] == team]['teamColor'].unique()[0]
st.pyplot(plot_shotmap(df_team, team, teamcolor))

#player = st.selectbox("Select a player", df[df['teamName'] == team]['playerName'].sort_values().unique(), index=0)

#op_team = st.selectbox("Against",df[df['playerName'] == player]['oppositeTeam'].sort_values().unique(),index=None)
#filtered_df = filter_data(df, team, player)