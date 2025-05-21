from utils import *
import random
import streamlit as st
import pandas as pd
import os,glob
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import psycopg2

st.title("Match Report")

league = st.selectbox(
    'Select League',
    ['Premier League', 'La Liga', 'Bundesliga', 'SerieA', 'Ligue1', 'Champions League', 'Europa League'],
    index=0
)

league_mapping = {
    'Premier League': 'premier-league',
    'La Liga': 'laliga',
    'Bundesliga': 'bundesliga',
    'SerieA': 'serie-a',
    'Ligue1': 'ligue-1',
    'Champions League': 'champions-league',
    'Europa League': 'europa-league'
}

# Use the mapping directly
mapped_league = league_mapping[league]

root_folder = f"D:/Scrape-Whoscored-Event-Data/data/{mapped_league}/"

df, csv_files = load_data(root_folder)

if df.empty:
    st.warning("No valid data could be loaded from CSV files.")
    st.stop()

df,teams = get_team_names(df)
home_team = st.selectbox('Select Home Team',teams,index=0)
away_team = st.selectbox('Select Away Team',teams,index=0)

match_df = get_match_df(df, home_team, away_team)
#print(match_df['matchId'].unique(),match_df['startDate'].unique())

viz = st.selectbox(
    'Select Visualization',
    ['Shot Map', 'Passing Network'],
    index=0
)

theme = st.selectbox(
    'Select Theme',
    ['Dark', 'Light'],
    index=0
)
if theme == 'Dark':
    background = "#051216F7"
    line_color = 'white'
    text_color = 'white'
else:
    background = "#FFFFFF"
    line_color = 'black'
    text_color = 'black'

if viz == 'Shot Map':
    #fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(20,22))
    pitch = Pitch(pitch_type='uefa',half=False, corner_arcs=True, pitch_color=background, line_color=line_color, linewidth=1.5)
    fig, axs = pitch.jointgrid(figheight=20,grid_width =1, left=None, bottom=None, grid_height=0.9,
                           axis=False,title_space=0,endnote_height=0,title_height=0,ax_top=False)
    fig.set_facecolor(background)
    home_team_col = match_df[match_df['teamName'] == home_team]['teamColor'].unique()[0]
    away_team_col = match_df[match_df['teamName'] == away_team]['teamColor'].unique()[0]
    summary_df,player_df = shotMap_ws(match_df,axs,fig,pitch,home_team,away_team,home_team_col,away_team_col,text_color,background)
    #shotMap(match_df,axs[1],away_team,'red')
    axs['pitch'].set_xlim(-10, 115)  # example: pitch length from 0 to 120
    axs['pitch'].set_ylim(-10, 80)   # example: pitch width from 0 to 80
    st.pyplot(fig)
    st.dataframe(summary_df, width=1000)
    st.dataframe(player_df, width=1000)
    


