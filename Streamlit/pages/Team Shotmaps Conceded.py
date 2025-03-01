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
import psycopg2

font_path = r'C:\Users\acer\Documents\GitHub\IndianCitizen\ScorePredict\Score Logos-20241022T100701Z-001\Score Logos\Sora_Font\Sora-Regular.ttf'
font_prop = fm.FontProperties(fname=font_path)
fm_sora = FontManager()

background='#0C0D0E'

def plot_shotmap_understat_conceded(df,team,league,teamcolor,situation,season):
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
        s=f'All shots conceded in the {league} {season}', 
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

st.title("Team ShotMaps - Conceded")
st.subheader("Analysizing Shots Conceded From Last 10 Seasons Across Top 5 Leagues")

# Database connection parameters
host = "localhost"
port = "5432"
database = "understat_shots_db"
user = "ichadha"
password = "ichadhapg"

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=host, port=port, database=database, user=user, password=password
    )
    st.success("Connected to PostgreSQL database!")
except Exception as e:
    st.error(f"Error connecting to the database: {e}")


season = st.selectbox('Select Season',[2024,2023,2022,2021,2020,2019,2018,2017,2016,2015,2014],index=0)

league = st.selectbox('Select League',['Premier League','La Liga','Bundesliga','SerieA','Ligue1'],index=0)

league_mapping = {
    'Premier League': 'EPL',
    'La Liga': 'La_Liga',
    'Bundesliga': 'Bundesliga',
    'SerieA': 'Serie_A',
    'Ligue1': 'Ligue_1'
}

# Get the mapped league value
db_league = league_mapping.get(league, league)


query = f"SELECT * FROM understat_shots_tb where league = '{db_league}' and season = {season};"
df = pd.read_sql(query, conn)

team = st.selectbox('Select Team',df['h_team'].sort_values().unique(),index=0)

number_of_colors = 1
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

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
plot_shotmap_understat_conceded(df, team,league, color[0],situation,season)