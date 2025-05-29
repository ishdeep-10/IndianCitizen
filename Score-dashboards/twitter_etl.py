import os
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry
import logging
from logging.handlers import RotatingFileHandler
import json
from collections import defaultdict
from utils import *

# Configure logging
def setup_logging():
    """Configure logging with both file and console handlers."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = logging.getLogger('twitter_etl')
    logger.setLevel(logging.DEBUG)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # File handler (rotating log files)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'twitter_etl.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    return logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logging()

# Configure rate limiting based on API limits
CALLS = 100  # API allows 100 calls per window
RATE_LIMIT = 3600  # one hour in seconds

class ETLStats:
    """Class to track ETL statistics."""
    def __init__(self):
        self.reset_stats()

    def reset_stats(self):
        """Reset all statistics."""
        self.tweets_processed = 0
        self.api_calls = 0
        self.errors = defaultdict(int)
        self.start_time = datetime.utcnow()
        self.accounts_stats = defaultdict(lambda: {
            'tweets_processed': 0,
            'api_calls': 0,
            'errors': 0
        })

    def log_stats(self):
        """Log current statistics."""
        duration = (datetime.utcnow() - self.start_time).total_seconds()
        stats = {
            'duration_seconds': duration,
            'tweets_per_second': self.tweets_processed / duration if duration > 0 else 0,
            'total_tweets': self.tweets_processed,
            'total_api_calls': self.api_calls,
            'errors': dict(self.errors),
            'accounts': dict(self.accounts_stats)
        }
        logger.info(f"ETL Stats: {json.dumps(stats, indent=2)}")

# Initialize stats tracker
stats = ETLStats()

def get_last_processed_date(conn: sqlite3.Connection) -> Optional[str]:
    """Get the last processed date from the database."""
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pipeline_state (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    conn.commit()

    cursor.execute('SELECT value FROM pipeline_state WHERE key = "last_processed_date"')
    result = cursor.fetchone()
    return result[0] if result else None

def update_last_processed_date(conn: sqlite3.Connection, date: str):
    """Update the last processed date in the database."""
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO pipeline_state (key, value)
    VALUES ("last_processed_date", ?)
    ''', (date,))
    conn.commit()

def normalize_datetime(date_str: str) -> str:
    """
    Normalize datetime string to consistent ISO format with UTC timezone.
    Handles various datetime formats and ensures consistent output.
    """
    try:
        # Remove any duplicate timezone indicators
        if '+00:00+00:00' in date_str:
            date_str = date_str.replace('+00:00+00:00', '+00:00')
        
        # Handle 'Z' timezone indicator
        if date_str.endswith('Z'):
            date_str = date_str[:-1]
        elif date_str.endswith('+00:00'):
            date_str = date_str[:-6]
        
        # Parse the datetime string
        dt = datetime.fromisoformat(date_str)
        
        # Return in consistent format with Z timezone indicator
        return f"{dt.strftime('%Y-%m-%dT%H:%M:%S')}Z"
    except Exception as e:
        logger.error(f"Error normalizing datetime {date_str}: {e}")
        raise ValueError(f"Invalid datetime format: {date_str}")

def get_date_window(current_date: str, is_historical: bool) -> tuple[str, str]:
    """
    Calculate the start and end dates for the current processing window.
    For historical loads, process one day at a time.
    For incremental loads, process from last processed to current-1.
    """
    try:
        # Remove Z or +00:00 for parsing
        clean_date = current_date.rstrip('Z').replace('+00:00', '')
        current = datetime.fromisoformat(clean_date)
        
        if is_historical:
            # For historical loads, process one day at a time
            end_date = (current + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        else:
            # For incremental loads, process up to yesterday
            end_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        
        # Return dates in ISO format with Z timezone indicator
        return f"{current.strftime('%Y-%m-%dT%H:%M:%S')}Z", f"{end_date}Z"
    except Exception as e:
        logger.error(f"Error calculating date window. Current date: {current_date}, Is historical: {is_historical}")
        logger.error(f"Error details: {e}")
        raise

def is_caught_up(current_date: str, target_date: str) -> bool:
    """Check if we've caught up to the target date."""
    try:
        # Remove Z or +00:00 for parsing
        current_clean = current_date.rstrip('Z').replace('+00:00', '')
        target_clean = target_date.rstrip('Z').replace('+00:00', '')
        
        current = datetime.fromisoformat(current_clean)
        target = datetime.fromisoformat(target_clean)
        return current >= target
    except Exception as e:
        logger.error(f"Error comparing dates. Current: {current_date}, Target: {target_date}")
        logger.error(f"Error details: {e}")
        raise

def get_pipeline_state(conn: sqlite3.Connection) -> Dict[str, str]:
    """Get the pipeline state from the database."""
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pipeline_state (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    conn.commit()

    cursor.execute('SELECT key, value FROM pipeline_state')
    return dict(cursor.fetchall())

def update_pipeline_state(conn: sqlite3.Connection, key: str, value: str):
    """Update a pipeline state value in the database."""
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR REPLACE INTO pipeline_state (key, value)
    VALUES (?, ?)
    ''', (key, value))
    conn.commit()

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def get_data(url: str, headers: dict, data: dict):
    """Make API call with retry logic and error handling."""
    try:
        stats.api_calls += 1
        account = data['usernames'][0]
        stats.accounts_stats[account]['api_calls'] += 1
        
        # Debug logging for API call
        logger.debug(f"Making API call to URL: {url}")
        logger.debug(f"Headers (API Key masked): {{'Content-Type': {headers.get('Content-Type')}, 'X-API-KEY': {'*' * 8}}}")
        logger.debug(f"Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=data)
        
        # Debug logging for response
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        logger.debug(f"Response content: {response.text[:1000]}")  # First 1000 chars to avoid huge logs
        
        response.raise_for_status()
        
        result = response.json()
        
        # Check response status
        if result.get('status') == 'warning':
            logger.warning(f"API returned warning status: {result.get('meta', {}).get('verification_message')}")
        
        # Extract tweets from response
        tweets = []
        if isinstance(result.get('data'), list):
            # Filter out empty or invalid tweets
            tweets = [
                tweet for tweet in result['data']
                if tweet.get('content') and  # Has content
                   tweet.get('tweet', {}).get('id') and  # Has tweet ID
                   tweet.get('user', {}).get('username')  # Has username
            ]
            
        if not tweets:
            logger.info(f"No valid tweets found for account {account} in the specified time window")
            return []
            
        logger.info(f"Found {len(tweets)} valid tweets in response")
        return tweets
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {e}"
        logger.error(error_msg)
        logger.error(f"Response content: {e.response.text}")
        stats.errors['http_errors'] += 1
        stats.accounts_stats[account]['errors'] += 1
        raise
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request Error: {e}"
        logger.error(error_msg)
        stats.errors['request_errors'] += 1
        stats.accounts_stats[account]['errors'] += 1
        raise

def transform_tweet(raw_tweet: Dict) -> Dict:
    """Transform raw tweet data into the desired format for database storage."""
    try:
        # If raw_tweet is a string, log it and raise an error
        if isinstance(raw_tweet, str):
            logger.error(f"Received string instead of dictionary: {raw_tweet}")
            raise ValueError("Tweet data must be a dictionary")

        # Log the raw tweet for debugging
        logger.debug(f"Processing raw tweet: {json.dumps(raw_tweet, indent=2)}")

        # Handle different response formats
        if isinstance(raw_tweet, dict):
            # Check if the tweet has the expected structure
            if 'user' in raw_tweet and 'tweet' in raw_tweet:
                user_data = raw_tweet.get('user', {})
                tweet_data = raw_tweet.get('tweet', {})
            else:
                # If the tweet doesn't have the expected structure, try to extract data from top level
                logger.warning(f"Unexpected tweet structure: {json.dumps(raw_tweet, indent=2)}")
                user_data = {
                    'username': raw_tweet.get('username'),
                    'display_name': raw_tweet.get('display_name'),
                    'id': raw_tweet.get('user_id'),
                    'verified': raw_tweet.get('verified'),
                    'followers_count': raw_tweet.get('followers_count'),
                    'following_count': raw_tweet.get('following_count')
                }
                tweet_data = {
                    'id': raw_tweet.get('id') or raw_tweet.get('tweet_id'),
                    'like_count': raw_tweet.get('like_count'),
                    'retweet_count': raw_tweet.get('retweet_count'),
                    'reply_count': raw_tweet.get('reply_count'),
                    'quote_count': raw_tweet.get('quote_count'),
                    'is_retweet': raw_tweet.get('is_retweet'),
                    'is_reply': raw_tweet.get('is_reply'),
                    'is_quote': raw_tweet.get('is_quote'),
                    'conversation_id': raw_tweet.get('conversation_id')
                }
        else:
            logger.error(f"Unexpected data type for tweet: {type(raw_tweet)}")
            raise ValueError(f"Tweet data must be a dictionary, got {type(raw_tweet)}")

        # Normalize datetime if present
        tweet_datetime = raw_tweet.get('datetime')
        if tweet_datetime:
            tweet_datetime = normalize_datetime(tweet_datetime)

        # Create transformed tweet with default values for all fields
        transformed_tweet = {
            'original_tweet_id': tweet_data.get('id'),
            'uri': raw_tweet.get('uri'),
            'datetime': tweet_datetime,
            'content': raw_tweet.get('content'),
            'username': user_data.get('username'),
            'display_name': user_data.get('display_name'),
            'user_id': user_data.get('id'),
            'verified': user_data.get('verified', False),
            'followers_count': user_data.get('followers_count', 0),
            'following_count': user_data.get('following_count', 0),
            'like_count': tweet_data.get('like_count', 0),
            'retweet_count': tweet_data.get('retweet_count', 0),
            'reply_count': tweet_data.get('reply_count', 0),
            'quote_count': tweet_data.get('quote_count', 0),
            'is_retweet': tweet_data.get('is_retweet', False),
            'is_reply': tweet_data.get('is_reply', False),
            'is_quote': tweet_data.get('is_quote', False),
            'conversation_id': tweet_data.get('conversation_id'),
            'in_reply_to_user_id': tweet_data.get('in_reply_to', {}).get('user_id'),
            'in_reply_to_username': tweet_data.get('in_reply_to', {}).get('username'),
            'processed_at': f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}Z"
        }

        # Log the transformed tweet for debugging
        logger.debug(f"Transformed tweet: {json.dumps(transformed_tweet, indent=2)}")

        # Validate required fields
        required_fields = ['original_tweet_id', 'datetime', 'content']
        missing_fields = [field for field in required_fields if not transformed_tweet.get(field)]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            logger.error(f"Raw tweet: {json.dumps(raw_tweet, indent=2)}")
            logger.error(f"Transformed tweet: {json.dumps(transformed_tweet, indent=2)}")
            raise ValueError(f"Missing required fields: {missing_fields}")

        return transformed_tweet
        
    except Exception as e:
        logger.error(f"Error transforming tweet: {str(e)}")
        logger.error(f"Raw tweet data: {json.dumps(raw_tweet, indent=2) if isinstance(raw_tweet, dict) else str(raw_tweet)}")
        stats.errors['transform_errors'] += 1
        raise

def init_database():
    """Initialize SQLite database and create table if it doesn't exist."""
    try:
        conn = sqlite3.connect('tweets.db')
        cursor = conn.cursor()
        
        # Enable foreign keys and optimize for better performance
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute('PRAGMA journal_mode = WAL')
        cursor.execute('PRAGMA synchronous = NORMAL')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_tweet_id TEXT UNIQUE,
            uri TEXT,
            datetime TEXT,
            content TEXT,
            username TEXT,
            display_name TEXT,
            user_id TEXT,
            verified BOOLEAN,
            followers_count INTEGER,
            following_count INTEGER,
            like_count INTEGER,
            retweet_count INTEGER,
            reply_count INTEGER,
            quote_count INTEGER,
            is_retweet BOOLEAN,
            is_reply BOOLEAN,
            is_quote BOOLEAN,
            conversation_id TEXT,
            in_reply_to_user_id TEXT,
            in_reply_to_username TEXT,
            processed_at TEXT
        )
        ''')
        
        # Create indexes for common queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_datetime ON tweets(datetime)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON tweets(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON tweets(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_original_tweet_id ON tweets(original_tweet_id)')
        
        conn.commit()
        return conn
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        stats.errors['db_errors'] += 1
        raise

def load_to_database(conn: sqlite3.Connection, tweet: Dict):
    """Load transformed tweet into the database."""
    try:
        cursor = conn.cursor()
        
        insert_query = '''
        INSERT OR REPLACE INTO tweets (
            original_tweet_id, uri, datetime, content, username, display_name,
            user_id, verified, followers_count, following_count,
            like_count, retweet_count, reply_count, quote_count,
            is_retweet, is_reply, is_quote, conversation_id,
            in_reply_to_user_id, in_reply_to_username, processed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(insert_query, (
            tweet['original_tweet_id'],
            tweet['uri'],
            tweet['datetime'],
            tweet['content'],
            tweet['username'],
            tweet['display_name'],
            tweet['user_id'],
            tweet['verified'],
            tweet['followers_count'],
            tweet['following_count'],
            tweet['like_count'],
            tweet['retweet_count'],
            tweet['reply_count'],
            tweet['quote_count'],
            tweet['is_retweet'],
            tweet['is_reply'],
            tweet['is_quote'],
            tweet['conversation_id'],
            tweet['in_reply_to_user_id'],
            tweet['in_reply_to_username'],
            tweet['processed_at']
        ))
        
        conn.commit()
        stats.tweets_processed += 1
        stats.accounts_stats[tweet['username']]['tweets_processed'] += 1
        
    except sqlite3.Error as e:
        logger.error(f"Database insertion error: {e}")
        logger.error(f"Tweet data: {json.dumps(tweet, indent=2)}")
        stats.errors['db_errors'] += 1
        raise

def run_etl_pipeline(url: str, headers: dict, start_date: str, accounts: List[str]):
    """Main ETL pipeline function."""
    conn = init_database()
    stats.reset_stats()
    
    try:
        # Get pipeline state
        state = get_pipeline_state(conn)
        current_date = state.get('last_processed_date', start_date)
        is_historical = state.get('mode', 'historical') == 'historical'
        
        # Normalize the start date to ISO format with Z
        current_date = normalize_datetime(current_date)
        
        # Log pipeline start
        logger.info(f"Starting ETL pipeline in {'historical' if is_historical else 'incremental'} mode")
        logger.info(f"Processing tweets from {current_date}")
        
        # Calculate target date (current date - 1 day) in ISO format with Z
        final_target_date = f"{(datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')}Z"
        
        while not is_caught_up(current_date, final_target_date):
            # Get the date window for this run
            window_start, window_end = get_date_window(current_date, is_historical)
            logger.info(f"Processing window: {window_start} to {window_end}")
            
            all_processed = True  # Flag to track if all accounts were fully processed
            
            for account in accounts:
                logger.info(f"Processing account: {account}")
                data = {
                    "source": "x",
                    "usernames": [account],
                    "limit": 1000,
                    "start_date": window_start,
                    "end_date": window_end
                }
                
                try:
                    raw_tweet_data = get_data(url, headers, data)
                    if raw_tweet_data:
                        # If we got maximum records, we might have more to process
                        if len(raw_tweet_data) == 1000:
                            all_processed = False
                            logger.warning(f"Hit 1000 tweet limit for {account} in current window")
                        
                        # Process tweets
                        successful_tweets = 0
                        for tweet in raw_tweet_data:
                            try:
                                transformed_tweet = transform_tweet(tweet)
                                load_to_database(conn, transformed_tweet)
                                successful_tweets += 1
                                logger.debug(f"Processed tweet {transformed_tweet['original_tweet_id']}")
                            except Exception as e:
                                logger.error(f"Error processing individual tweet: {e}")
                                stats.errors['tweet_processing_errors'] += 1
                                continue
                        
                        logger.info(f"Successfully processed {successful_tweets} out of {len(raw_tweet_data)} tweets for {account}")
                    else:
                        logger.info(f"No tweets found for {account} in current window")
                    
                except Exception as e:
                    logger.error(f"Error processing account {account}: {e}")
                    all_processed = False
                    stats.errors['account_processing_errors'] += 1
                    continue
            
            # Update the current date based on whether we fully processed the window
            if all_processed:
                # Move to the next day if we processed everything
                current_date = window_end
                update_pipeline_state(conn, 'last_processed_date', current_date)
                logger.info(f"Completed processing window, moving to {current_date}")
                
                # Check if we should switch to incremental mode
                if is_historical and is_caught_up(current_date, final_target_date):
                    is_historical = False
                    update_pipeline_state(conn, 'mode', 'incremental')
                    logger.info("🎉 Historical load complete! Switching to incremental mode")
                    logger.info(f"Historical load processed from {start_date} to {current_date}")
            else:
                # If we hit the rate limit or didn't process everything, 
                # we'll try again in the next run
                logger.warning(f"Incomplete window processing. Will resume from {current_date}")
                break
            
        # Log final statistics
        stats.log_stats()
        
    except Exception as e:
        logger.error(f"Critical error in ETL pipeline: {e}", exc_info=True)
        stats.errors['critical_errors'] += 1
        raise
    finally:
        stats.log_stats()
        conn.close()

if __name__ == "__main__":
    # Load and verify environment variables
    load_dotenv()
    
    api_key = os.getenv("MAINNET_API_KEY")
    api_url = os.getenv("MAINNET_API_URL")
    
    if not api_key or not api_url:
        logger.error("Missing required environment variables:")
        if not api_key:
            logger.error("- MAINNET_API_KEY is not set")
        if not api_url:
            logger.error("- MAINNET_API_URL is not set")
        raise ValueError("Missing required environment variables")
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': api_key
    }

    url = f'{api_url}/api/v1/on_demand_data_request'
    
    # List of Twitter/X accounts to monitor
    target_accounts = [
        # Add your target accounts here
        "@AndyRobsonTips","@JamesMurphyTips","@MarkOHaire","@TheFootieGuys","@predictzcom"
    ]

    # Initial start date for historical data
    start_date = "2025-05-26T00:00:00Z"
    
    run_etl_pipeline(url, headers, start_date, target_accounts) 