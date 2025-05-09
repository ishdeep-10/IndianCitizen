import pandas as pd
import requests
from sqlalchemy import create_engine
import datetime
import understatapi
#import papermill as pm
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Database connection settings (replace with your credentials)
db_config = {
    'dbname': 'understat_db',
    'user': 'ishdeep',
    'password': 'ichadhapg',
    'host': 'localhost',
    'port': 5432,
}
engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}")

def save_to_postgres(dataframe, table_name):
    try:
        dataframe.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Data successfully saved to {table_name} table.")
    except Exception as e:
        print(f"Error saving data to PostgreSQL: {e}")

def extract_and_save_shots(league, season):
    client = understatapi.UnderstatClient()

    # Fetch match data
    league_data = client.league(league=league).get_match_data(season=season)
    matches = []

    for match in league_data:
        matches.append({
            'id': match['id'],
            'home_team': match['h']['title'],
            'away_team': match['a']['title'],
            'home_goals': match['goals']['h'],
            'away_goals': match['goals']['a'],
            'home_xG': match['xG']['h'],
            'away_xG': match['xG']['a'],
            'datetime': match['datetime']
        })

    matches_df = pd.DataFrame(matches)
    all_shot_data = []

    current_timestamp = datetime.datetime.now().timestamp()

    for _, row in matches_df.iterrows():
        match_timestamp = pd.to_datetime(row['datetime']).timestamp()
        if match_timestamp <= current_timestamp:
            try:
                shot_data = client.match(match=row['id']).get_shot_data()
                all_shot_data.append(shot_data)
            except Exception as e:
                print(f"Error fetching shot data: {e}")

    compiled_shot_data = []
    for match in all_shot_data:
        for shot in match.get('h', []):
            shot['h_a'] = 'h'
            compiled_shot_data.append(shot)
        for shot in match.get('a', []):
            shot['h_a'] = 'a'
            compiled_shot_data.append(shot)

    compiled_shot_df = pd.DataFrame(compiled_shot_data)
    compiled_shot_df['league'] = league
    compiled_shot_df['season'] = season

    save_to_postgres(compiled_shot_df, 'understat_shots_tb')

# Airflow DAG definition
default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'extract_understat_data',
    default_args=default_args,
    description='Extract and save Understat shot data',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

run_shot_extraction = PythonOperator(
    task_id='run_shot_extraction',
    python_callable=extract_and_save_shots,
    op_kwargs={'league': 'EPL', 'season': '2024'},
    dag=dag,
)
