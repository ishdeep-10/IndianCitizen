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
import matplotlib.font_manager as font_manager
import matplotlib.image as mpimg
import matplotlib.patches as patches
import soccerdata as sd
from unidecode import unidecode

def filter_data(df: pd.DataFrame, team: str, player: str):
    if team:
        df = df[df['teamName'] == team]
    if player:
        df = df[df['playerName'] == player]
    return df

def plot_shots(df, ax, pitch):
    for row in df.to_dict(orient='records'):
        pitch.scatter(
            x=row['x'],
            y=row['y'],
            ax=ax,
            s=1000 * row['expectedGoals'],
            color='green' if row['eventType'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if row['eventType'] == 'Goal' else .5,
            zorder=2 if row['eventType'] == 'Goal' else 1
        )


st.title("Premier League 2024 ShotMap")
st.subheader("Filter to any team or player to see shots taken")

df = pd.read_csv('C:/Users/acer/Documents/GitHub/IndianCitizen/StreamLit/Data/2024-25/PL/premier_league_2024-25_shot_data.csv')
#print(df.head())

team = st.selectbox('Select Team',df['teamName'].sort_values().unique(),index=None)
player = st.selectbox("Select a player", df[df['teamName'] == team]['playerName'].sort_values().unique(), index=None)

#op_team = st.selectbox("Against",df[df['playerName'] == player]['oppositeTeam'].sort_values().unique(),index=None)
filtered_df = filter_data(df, team, player)


pitch = VerticalPitch(pitch_type='custom',pitch_length = 105,pitch_width = 68, line_zorder=2, pitch_color='#0C0D0E', line_color='white', half=True)
fig, ax = pitch.draw(figsize=(10, 10))
background_color='#0C0D0E'

plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)