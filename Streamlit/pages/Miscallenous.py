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
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

font_path = r'C:\Users\acer\Documents\GitHub\IndianCitizen\ScorePredict\Score Logos-20241022T100701Z-001\Score Logos\Sora_Font\Sora-Regular.ttf'
font_prop = fm.FontProperties(fname=font_path)
fm_sora = FontManager()



def top9_shots_europe(df_stats,df_shots):
    df = df_shots.copy()
    df['X'] = (df['X'] / 100) * 105 * 100
    df['Y'] = (df['Y'] / 100) * 68 * 100
    plt.rcParams['hatch.linewidth'] = 0.02
    plt.rcParams['font.family'] = 'serif'
    plt.style.use('fivethirtyeight')
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(18,30), dpi=300)
    background='#0C0D0E'
    fig.patch.set_facecolor(background)
    
    axs = axs.flatten()  # Flatten the axis array for easy iteration

    img_url = 'C:\\Users\\acer\\Documents\\GitHub\\IndianCitizen\\ScorePredict\\Images\\TeamLogos'
    for index, ax in enumerate(axs):
        pitch = VerticalPitch(
        pitch_type='uefa',
        goal_type = 'line',
        half=True, 
        pitch_color=background, 
        stripe=False, 
        line_color='white',
        linewidth=1,
        line_zorder=2,pad_bottom=0, pad_top=20
        )
        pitch.draw(ax=ax)
        
        ax.annotate(text=f"{df_stats['player'].iloc[index].upper()}", xy=(32, 120), size=20, color='white', ha='center', va='center', font=font_prop)
        team_name = df_stats['team'].iloc[index]
        img = plt.imread(f"{img_url}\\{team_name}.png")  # Adjust file path as needed
        im = OffsetImage(img, zoom=0.35)  # Adjust zoom for size
        ab = AnnotationBbox(
            im, 
            (65, 117),  # Adjust coordinates for image placement
            frameon=False,
            xycoords='data'
        )
        ax.add_artist(ab)
        
        
        ax.annotate(text=f"Shots - {df_stats['num_shots'].iloc[index]} ", xy=(45, 113), size=18, color='white', ha='center', va='center', font=font_prop)

        ax.annotate(text=f" | Shots OT - {df_stats['num_shots_on_target'].iloc[index]}", xy=(22, 113), size=18, color='white', ha='center', va='center', font=font_prop)

        player_shots = df[df['player'] == df_stats['player'].iloc[index]]

        if not player_shots.empty:
            # Plot hexbin for the player's shots
            pitch.hexbin(
                player_shots.X, 
                player_shots.Y, 
                ax=ax, 
                edgecolors='white',
                gridsize=(14, 14), 
                cmap='summer', 
                alpha=0.7, 
                zorder=3
            )

        player_goals = player_shots[(player_shots['result'] == 'Goal') & (player_shots['situation'] != 'Penalty')]
        pitch.scatter(player_goals.X, player_goals.Y,s=150, ax=ax, zorder=4, edgecolors='#DE8A04',marker='football',
                            alpha=0.9, linewidths=1.2, c=background)

        pitch.scatter(65, 55,s=2800, ax=ax, zorder=4, edgecolors='#DE8A04',alpha=0.9, lw=1.5, color=background)
        pitch.scatter(65, 35,s=2800, ax=ax, zorder=4, edgecolors='#DE8A04',alpha=0.9, lw=1.5, color=background)
        pitch.scatter(65, 15,s=2800, ax=ax, zorder=4, edgecolors='#DE8A04',alpha=0.9, lw=1.5, color=background)

        pitch.annotate(text=f"{df_stats['num_goals'].iloc[index]}",ax=ax, xy=(65, 55), size=18, color='white', ha='center', va='center',zorder=5, font=font_prop)
        pitch.annotate(text="Goals",ax=ax, xy=(57, 55), size=18, color='white', ha='center', va='center',zorder=5, font=font_prop)

        pitch.annotate(text=f"{df_stats['total_xg'].iloc[index]}",ax=ax, xy=(65, 35), size=16, color='white', ha='center', va='center',zorder=5, font=font_prop)
        pitch.annotate(text="xG",ax=ax, xy=(57, 35), size=18, color='white', ha='center', va='center',zorder=5, font=font_prop)

        pitch.annotate(text=f"{df_stats['total_npxg'].iloc[index]}",ax=ax, xy=(65, 15), size=16, color='white', ha='center', va='center',zorder=5, font=font_prop)
        pitch.annotate(text="npxG",ax=ax, xy=(57, 15), size=18, color='white', ha='center', va='center',zorder=5, font=font_prop)

    #fig.patch.set_facecolor(background)
    plt.subplots_adjust(wspace=0, hspace=-0.6)

    fig.text(x=0.51, y=0.78, s=f"Top 9 Players By Shots", va="bottom", ha="center",
                fontsize=35, color="white", font=font_prop, weight="bold")
    fig.text(x=0.51, y=0.76, s=f"Across Top 5 Leagues | Season 2024/25 | @wearescore",color="white",
            va="bottom", ha="center", fontsize=22, font=font_prop)
    
    st.pyplot(fig)

st.title("Miscallenous Plots")

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

viz = st.selectbox('Select Plot',['Top 9 Players'],index=0)
league = st.selectbox('Select League',['All Leagues','Premier League','La Liga','Bundesliga','SerieA','Ligue1'],index=0)

league_mapping = {
    'All Leagues' : 'All Leagues',
    'Premier League': 'EPL',
    'La Liga': 'La_Liga',
    'Bundesliga': 'Bundesliga',
    'SerieA': 'Serie_A',
    'Ligue1': 'Ligue_1'
}

# Get the mapped league value
db_league = league_mapping.get(league, league)

season = st.selectbox('Select Season',[2024,2023,2022,2021,2020,2019,2018,2017,2016,2015,2014],index=0)

query = """
select player , count(*) as num_shots,count(case when "result" = 'Goal' or "result" = 'SavedShot' or "result" = 'ShotOnPost' then 1 else null end) as num_shots_on_target,
count(case when "result" = 'Goal' then 1 else null end) as num_goals,
count(case when "result" = 'Goal' and situation != 'Penalty' then 1 else null end) as num_goals_non_penalty,
sum(round("xG" :: numeric ,2)) as total_xG,
sum(case when situation != 'Penalty' then round("xG" :: numeric ,2) else null end) as total_npxG
from understat_shots_tb ust
where season = '2024'
group by player
order by num_shots desc
limit 9;"""
df_stats = pd.read_sql(query, conn)
df_stats['team'] = ['Real Madrid','Man City','Bournemouth','Lecce','Frankfurt','Barcelona','Barcelona','Lazio','Chelsea']

query_shots = """
select "result","X","Y",situation,"shotType",player from understat_shots_tb ust
where season = '2024' and 
player in (select player from

(select player , count(*) as num_shots,
count(case when "result" = 'Goal' or "result" = 'SavedShot' or "result" = 'ShotOnPost' then 1 else null end) as num_shots_on_target,
count(case when "result" = 'Goal' then 1 else null end) as num_goals,
count(case when "result" = 'Goal' and situation != 'Penalty' then 1 else null end) as num_goals_non_penalty,
sum(round("xG" :: numeric ,2)) as total_xG,
sum(case when situation != 'Penalty' then round("xG" :: numeric ,2) else null end) as total_npxG
from understat_shots_tb ust
where season = '2024'
group by player
order by num_shots desc
limit 9) players);"""

df_shots = pd.read_sql(query_shots, conn)
#st.dataframe(df_shots)
top9_shots_europe(df_stats,df_shots)