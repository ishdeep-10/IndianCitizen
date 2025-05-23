from utils import *
import random
import streamlit as st
import pandas as pd
import os,glob
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import psycopg2


team_dict = { 
        65: 'Barcelona',
        63: 'Atletico Madrid',
        52: 'Real Madrid',
        53: 'Atletic Club',
        839: 'Villarreal',
        54: 'Real Betis',
        64: 'Rayo Vallecano',
        51: 'Mallorca',
        68: 'Real Sociedad',
        62: 'Celta Vigo',
        131: 'Osasuna',
        67: 'Sevilla',
        2783: 'Girona',
        819: 'Getafe',
        70: 'Espanyol',
        825: 'Leganes',
        838: 'Las Palmas',
        55 : 'Valencia',
        60 : 'Deportivo Alaves',
        58: 'Real Valladolid',
        13: 'Arsenal',
        161: 'Wolves',
        24: 'Aston Villa',
        211: 'Brighton',
        30: 'Tottenham',
        167: 'Man City',
        14: 'Leicester',
        18: 'Southampton',
        183: 'Bournemouth',
        26: 'Liverpool',
        23: 'Newcastle',
        15: 'Chelsea',
        174: 'Nottingham Forest',
        29: 'West Ham',
        32: 'Man Utd',
        170: 'Fulham',
        189: 'Brentford',
        162: 'Crystal Palace',
        31: 'Everton',
        165: 'Ipswich',
        37: 'Bayern Munich',
        36: 'Bayer Leverkusen',
        45: 'Eintracht Frankfurt',
        219: 'Mainz 05',
        50: 'Freiburg',
        7614: 'RB Leipzig',
        33: 'Wolfsburg',
        134: 'Borussia M.Gladbach',
        41: 'VfB Stuttgart',
        44: 'Borussia Dortmund',
        1730: 'Augsburg',
        42: 'Werder Bremen',
        1211: 'Hoffenheim',
        796: 'Union Berlin',
        283: 'St. Pauli',
        1206: 'Holstein Kiel',
        4852: 'FC Heidenheim',
        109: 'Bochum',
        75 : 'Inter',
        276 : 'Napoli',
        300 : 'Atalanta',
        87 : 'Juventus',
        77 : 'Lazio',
        71 : 'Bologna',
        73 : 'Fiorentina',
        84 : 'Roma',
        80 : 'AC Milan',
        86 : 'Udinese',
        72 : 'Torino',
        278 : 'Genoa',
        1290 : 'Como',
        76 : 'Verona',
        78 : 'Cagliari',
        79 : 'Lecce',
        24341 : 'Parma Calcio',
        272 : 'Empoli',
        85 : 'Venezia',
        269 : 'Monza',
        304 : 'PSG',
        249 : 'Marseille',
        613 : 'Nice',
        248 : 'Monaco',
        607 : 'Lille',
        228 : 'Lyon',
        148 : 'Strasbourg',
        246 : 'Toulouse',
        309 : 'Lens',
        2332 : 'Brest',
        313 : 'Rennes',
        308 : 'Auxerre',
        614 : 'Angers',
        302 : 'Nantes',
        950 : 'Reims',
        217 : 'Le Havre',
        145 : 'Saint-Etienne',
        311 : 'Montpellier',
        299 : 'Benfica',
        129 : 'PSV'
    }
    
team_colors = {
    'Barcelona': '#A50044',
    'Atletico Madrid': '#CE3524',
    'Real Madrid': '#FCBF00',
    'Athletic Club': '#E0092C',
    'Villarreal': '#FFE667',
    'Real Betis': '#0BB363',
    'Rayo Vallecano': '#E53027',
    'Mallorca': '#E20613',
    'Real Sociedad': '#0067B1',
    'Celta Vigo': '#8AC3EE',
    'Osasuna': '#E60026',
    'Sevilla': '#D00027',
    'Girona': '#DA291C',
    'Getafe': '#003DA5',
    'Espanyol': '#00529F',
    'Leganes': '#005BAC',
    'Las Palmas': '#FEDD00',
    'Valencia': '#F18E00',
    'Deportivo Alaves': '#005BAC',
    'Real Valladolid': '#7A1E8B',
    'Arsenal': '#EF0107',
    'Wolves': '#FDB913',
    'Aston Villa': '#95BFE5',
    'Brighton': '#0057B8',
    'Tottenham': '#132257',
    'Man City': '#6CABDD',
    'Leicester': '#003090',
    'Southampton': '#D71920',
    'Bournemouth': '#DA291C',
    'Liverpool': '#C8102E',
    'Newcastle': "#F8F5F6",
    'Chelsea': '#034694',
    'Nottingham Forest': '#E53233',
    'West Ham': '#7A263A',
    'Man Utd': '#DA291C',
    'Fulham': "#FFFFFF",
    'Brentford': '#E30613',
    'Crystal Palace': '#1B458F',
    'Everton': '#003399',
    'Ipswich': '#005BAC',
    'Bayern Munich': '#DC052D',
    'Bayer Leverkusen': '#E30613',
    'Eintracht Frankfurt': "#FFFFFF",
    'Mainz 05': '#C8102E',
    'Freiburg': "#F9F4F4",
    'RB Leipzig': '#E4002B',
    'Wolfsburg': '#65B32E',
    'Borussia M.Gladbach': "#EEF3ED",
    'VfB Stuttgart': '#E30613',
    'Borussia Dortmund': '#FDE100',
    'Augsburg': '#C8102E',
    'Werder Bremen': '#1A9F3D',
    'Hoffenheim': '#005BAC',
    'Union Berlin': '#E30613',
    'St. Pauli': '#A45A2A',
    'Holstein Kiel': '#005BAC',
    'FC Heidenheim': '#E30613',
    'Bochum': '#005BAC',
    'Inter': '#1E2943',
    'Napoli': '#0082CA',
    'Atalanta': '#1C1C1C',
    'Juventus': "#F8F4F4",
    'Lazio': '#A8C6E5',
    'Bologna': '#D4001F',
    'Fiorentina': '#592C82',
    'Roma': '#8E1111',
    'AC Milan': '#FB090B',
    'Udinese': "#F2EBEB",
    'Torino': '#8B1B3A',
    'Genoa': '#C8102E',
    'Como': '#005BAC',
    'Verona': '#FCE500',
    'Cagliari': '#C8102E',
    'Lecce': '#FCE500',
    'Parma Calcio': '#FCE500',
    'Empoli': '#005BAC',
    'Venezia': "#F2ECEC",
    'Monza': '#E30613',
    'PSG': '#004170',
    'Marseille': '#009DDC',
    'Nice': '#E30613',
    'Monaco': '#ED1C24',
    'Lille': '#E30613',
    'Lyon': '#E30613',
    'Strasbourg': '#005BAC',
    'Toulouse': '#5F259F',
    'Lens': '#E30613',
    'Brest': '#E30613',
    'Rennes': '#E30613',
    'Auxerre': '#005BAC',
    'Angers': "#EEECEC",
    'Nantes': '#FCE500',
    'Reims': '#E30613',
    'Le Havre': '#005BAC',
    'Saint-Etienne': '#009639',
    'Montpellier': '#005BAC',
    'Benfica': '#E30613',
    'PSV': '#E30613',
    'Ajax': '#E30613',
    'Feyenoord': '#E30613',
    'Utrecht': '#E30613',
    'AZ-Alkmaar': '#E30613',
    'Twente': '#E30613',
    'Go Ahead Eagles': '#E30613',
    'FC Groningen': '#007A33',
    'Fortuna Sittard': '#FCE500',
    'Heracles': "#FAF7F7",
    'SC Heerenveen': '#005BAC',
    'NEC Nijmegen': '#E30613',
    'NAC Breda': '#FCE500',
    'PEC Zwolle': '#005BAC',
    'Sparta Rotterdam': '#E30613',
    'Willem II': '#E30613',
    'RKC Waalwijk': '#FCE500',
    'Almere City': '#E30613'
    }

# Set the path to the locally downloaded font file
font_path = r'C:\Users\acer\Documents\GitHub\IndianCitizen\ScorePredict\Score Logos-20241022T100701Z-001\Score Logos\Sora_Font\Sora-Regular.ttf'

# Add the font to matplotlib
font_prop = fm.FontProperties(fname=font_path)
st.set_page_config(layout="centered")

st.title("Match Report")

theme = st.radio(
    '',
    options=['🌙 Dark', '☀️ Light'],
    index=0,
    horizontal=True
)

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

df,teams = get_team_names(df,team_dict,team_colors)
col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox('Select Home Team', teams, index=0)

with col2:
    away_team = st.selectbox('Select Away Team', teams, index=0)


match_df = get_match_df(df, home_team, away_team,team_dict,team_colors)
#match_df = match_df.sort_values(by='id').reset_index(drop=True)
home_team_col = match_df[match_df['teamName'] == home_team]['teamColor'].unique()[0]
away_team_col = match_df[match_df['teamName'] == away_team]['teamColor'].unique()[0]
#print(match_df['matchId'].unique(),match_df['startDate'].unique())

## Shots - ShotMap , xG Flow , OnGoal Shots
## Passing - Passing Network , Average On Ball Positions - Passes Played , Passes Received


viz = st.selectbox(
    'Select Action',
    ['Shots', 'In Possession'],
    index=0
)

if theme == '🌙 Dark':
    background = "#010b14"
    line_color = 'white'
    text_color = 'white'
    logo = mpimg.imread('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Score Logos-20241022T100701Z-001/Score Logos/ScoreSquareWhite.png')

else:
    background = "#FFFFFF"
    line_color = 'black'
    text_color = 'black'
    logo = mpimg.imread('C:/Users/acer/Documents/GitHub/IndianCitizen/ScorePredict/Score Logos-20241022T100701Z-001/Score Logos/ScoreSquareDark.png')


if viz == 'Shots':
    #fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(20,22))
    pitch = Pitch(pitch_type='uefa',half=False, corner_arcs=True, pitch_color=background, line_color=line_color, linewidth=1.5)
    fig, axs = pitch.jointgrid(figheight=20,grid_width =1, left=None, bottom=None, grid_height=0.9,
                           axis=False,title_space=0,endnote_height=0,title_height=0,ax_top=False)
    fig.set_facecolor(background)
    
    summary_df,player_df,home_shots_df,away_shots_df = shotMap_ws(match_df,axs,fig,pitch,home_team,away_team,home_team_col,away_team_col,text_color,background)
    #shotMap(match_df,axs[1],away_team,'red')
    axs['pitch'].set_xlim(-10, 115)  # example: pitch length from 0 to 120
    axs['pitch'].set_ylim(-10, 80)   # example: pitch width from 0 to 80
    st.pyplot(fig)
    st.dataframe(summary_df, width=1000)
    st.dataframe(player_df, width=1000)

    fig2, axs2 = plt.subplots(nrows=1, ncols=1, figsize=(20,12))
    fig2.set_facecolor(background)

    ax_image = add_image(
        logo, fig2, left=0.83, bottom=0.88, width=0.08, height=0.08,aspect='equal'
    )

    xgFlow(axs2,home_shots_df,away_shots_df,home_team,away_team,home_team_col,away_team_col,text_color,background)
    st.pyplot(fig2)

if viz == 'In Possession':
    passes_df = get_passes_df(match_df)
    team = st.radio('',options=[home_team, away_team],index=0,horizontal=True)
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(20,15))
    fig.set_facecolor(background)
    
    ax_image = add_image(
        logo, fig, left=0.82, bottom=0.83, width=0.07, height=0.07,aspect='equal'
    )
    if team == home_team:
        
        minute_of_subs = match_df[(match_df['teamName'] == home_team) & (match_df['type'] == 'SubstitutionOn')]['minute'].unique()
        minute_of_subs.sort()  # Ensure they're in order
        minute_of_subs = minute_of_subs[minute_of_subs < 90]
        def ordinal(n):
            return ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth'][n - 1]

        # Build dynamic options list
        options = ['Starting 11']
        for i in range(len(minute_of_subs)):
            options.append(f'{ordinal(i+1)} Substitution')

        # Radio selector with dynamic options
        substitutions = st.radio('', options=options, index=0, horizontal=True)
        # Get minute_start and minute_end
        if substitutions == 'Starting 11':
            minute_start = 0
            minute_end = minute_of_subs[0] if len(minute_of_subs) > 0 else 90
        else:
            index = options.index(substitutions) - 1  # subtract 1 to match substitution index
            minute_start = minute_of_subs[index]
            minute_end = minute_of_subs[index + 1] if index + 1 < len(minute_of_subs) else 90
        print(minute_start,minute_end)
        fig.text(
        0.16, 0.86, f"Passing Networks {minute_start}-{minute_end}",fontproperties=font_prop,
        ha='left', va='center', fontsize=45, color=text_color
        )
        filtered_passes_df = filter_passes_for_subwindow(match_df, passes_df, home_team, minute_start, minute_end)

        home_passes_between_df, home_average_locs_and_count_df = get_passes_between_df(home_team, filtered_passes_df)
        ci = calculate_centralization_index(home_team,filtered_passes_df)
        pass_network_visualization(axs, match_df, home_passes_between_df, home_average_locs_and_count_df, text_color, background, home_team_col, home_team, 20, False,ci)
        st.pyplot(fig)


        fig2,ax2 = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
        fig2.set_facecolor(background)
        pass_matrix = get_pass_matrix(passes_df, home_team)
        custom_cmap = LinearSegmentedColormap.from_list("custom_green", [background, home_team_col])
        annotations = pass_matrix.map(lambda x: f"{x}" if x >= 5 else "")
        sns.heatmap(pass_matrix, annot=annotations, cmap=custom_cmap, fmt='', linewidths=1, square=True,cbar=False,annot_kws={"size": 14},ax=ax2)

        #ax.set_title('Pass Combination Matrix')
        ax2.set_xlabel('Receiver', fontproperties=font_prop,fontsize=18, color=text_color)
        ax2.set_ylabel('Passer', fontproperties=font_prop,fontsize=18, color=text_color)
        plt.xticks(rotation=90, fontproperties=font_prop,fontsize=12, color=text_color)
        plt.yticks(rotation=0, fontproperties=font_prop,fontsize=12, color=text_color)
        st.pyplot(fig2)
    else:
        minute_of_subs = match_df[(match_df['teamName'] == away_team) & (match_df['type'] == 'SubstitutionOn')]['minute'].unique()
        minute_of_subs.sort()  # Ensure they're in order
        minute_of_subs = minute_of_subs[minute_of_subs < 90]
        def ordinal(n):
            return ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth'][n - 1]

        # Build dynamic options list
        options = ['Starting 11']
        for i in range(len(minute_of_subs)):
            options.append(f'{ordinal(i+1)} Substitution')

        # Radio selector with dynamic options
        substitutions = st.radio('', options=options, index=0, horizontal=True)
        # Get minute_start and minute_end
        if substitutions == 'Starting 11':
            minute_start = 0
            minute_end = minute_of_subs[0] if len(minute_of_subs) > 0 else 90
        else:
            index = options.index(substitutions) - 1  # subtract 1 to match substitution index
            minute_start = minute_of_subs[index]
            minute_end = minute_of_subs[index + 1] if index + 1 < len(minute_of_subs) else 90
        print(minute_start,minute_end)
        fig.text(
        0.16, 0.86, f"Passing Networks {minute_start}-{minute_end}",fontproperties=font_prop,
        ha='left', va='center', fontsize=45, color=text_color
        )
        filtered_passes_df = filter_passes_for_subwindow(match_df, passes_df, away_team, minute_start, minute_end)

        away_passes_between_df, away_average_locs_and_count_df = get_passes_between_df(away_team, filtered_passes_df)
        ci = calculate_centralization_index(away_team,filtered_passes_df)
        pass_network_visualization(axs, match_df, away_passes_between_df, away_average_locs_and_count_df, text_color, background, away_team_col, away_team, 20, False,ci)
        st.pyplot(fig)

        fig2,ax2 = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
        fig2.set_facecolor(background)
        pass_matrix = get_pass_matrix(passes_df, away_team)
        custom_cmap = LinearSegmentedColormap.from_list("custom_green", [background, away_team_col])
        annotations = pass_matrix.map(lambda x: f"{x}" if x >= 5 else "")
        sns.heatmap(pass_matrix, annot=annotations, cmap=custom_cmap, fmt='', linewidths=1, square=True,cbar=False,annot_kws={"size": 14},ax=ax2)

        #ax.set_title('Pass Combination Matrix')
        ax2.set_xlabel('Receiver', fontproperties=font_prop,fontsize=18, color=text_color)
        ax2.set_ylabel('Passer', fontproperties=font_prop,fontsize=18, color=text_color)
        plt.xticks(rotation=90, fontproperties=font_prop,fontsize=12, color=text_color)
        plt.yticks(rotation=0, fontproperties=font_prop,fontsize=12, color=text_color)
        st.pyplot(fig2)


    

