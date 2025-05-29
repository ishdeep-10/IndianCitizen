import random
import streamlit as st
import pandas as pd
import psycopg2
from utils import plot_shotmap_understat_conceded


st.title("Team ShotMaps - Conceded")
st.subheader("Analysizing Shots Conceded From Last 10 Seasons Across Top 5 Leagues")

# Database connection parameters
host = "localhost"
port = "5432"
database = "understat_db"
user = "ishdeep"
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