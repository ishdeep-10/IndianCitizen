# Twitter Data Ingestion Pipeline

This project implements a data ingestion pipeline that extracts tweets from Twitter/X accounts, transforms the data, and loads it into a SQLite database.

## Features

- Rate-limited API calls (1000 calls per hour)
- SQLite database storage
- ETL pipeline with error handling
- Environment variable configuration

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy `.env.template` to `.env` and fill in your Twitter/X API credentials:
```bash
cp .env.template .env
```

4. Edit the `.env` file with your Twitter/X API credentials

## Usage

1. Edit the `target_accounts` list in `twitter_etl.py` to include the Twitter/X accounts you want to monitor
2. Run the pipeline:
```bash
python twitter_etl.py
```

## Database Schema

The tweets are stored in a SQLite database (`tweets.db`) with the following schema:

- `tweet_id`: Unique identifier for the tweet (Primary Key)
- `text`: The tweet content
- `created_at`: Tweet creation timestamp
- `author_id`: ID of the tweet author
- `retweet_count`: Number of retweets
- `like_count`: Number of likes
- `reply_count`: Number of replies
- `processed_at`: Timestamp when the tweet was processed

## Rate Limiting

The pipeline is configured to respect Twitter's rate limit of 1000 calls per hour. The `@limits` and `@sleep_and_retry` decorators ensure that the API calls are properly throttled. 