import requests
import json
from dotenv import load_dotenv
import os
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

# Configure logging
def setup_logging():
    """Configure logging with both file and console handlers."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = logging.getLogger('transfers_etl')
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
        os.path.join(log_dir, 'transfers_etl.log'),
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

def init_database():
    """Initialize SQLite database and create transfers table if it doesn't exist."""
    try:
        conn = sqlite3.connect('sportmonks.db')
        cursor = conn.cursor()
        
        # Enable foreign keys and optimize for better performance
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute('PRAGMA journal_mode = WAL')
        cursor.execute('PRAGMA synchronous = NORMAL')
        
        # Create transfers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transfer_id INTEGER UNIQUE,
            sport_id INTEGER,
            player_id INTEGER,
            type_id INTEGER,
            from_team_id INTEGER,
            to_team_id INTEGER,
            position_id INTEGER,
            detailed_position_id INTEGER,
            date TEXT,
            career_ended BOOLEAN,
            completed BOOLEAN,
            amount REAL,
            currency TEXT,
            player_name TEXT,
            player_common_name TEXT,
            from_team_name TEXT,
            from_team_short_code TEXT,
            to_team_name TEXT,
            to_team_short_code TEXT,
            processed_at TEXT
        )
        ''')
        
        # Create indexes for common queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transfer_date ON transfers(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_id ON transfers(player_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_from_team_id ON transfers(from_team_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_to_team_id ON transfers(to_team_id)')
        
        conn.commit()
        return conn
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise

def fetch_latest_transfers(startDate, endDate):
    """Fetch latest transfers from the SportMonks API."""
    all_transfers = []
    next_page = f"https://api.sportmonks.com/v3/football/transfers/between/{startDate}/{endDate}"
    page_count = 0

    while next_page:
        page_count += 1
        logger.info(f"Fetching page {page_count} from {next_page}")

        params = {"api_token": sportmonks_key,"include":"player;fromTeam;toTeam","per_page":50}
        try:
            response = requests.get(next_page, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Log the response structure for debugging
            logger.debug(f"API Response: {json.dumps(data, indent=2)}")
            
            # Check for error response
            if "errors" in data:
                logger.error(f"API returned errors: {json.dumps(data['errors'], indent=2)}")
                break
                
            # Check response structure
            if not isinstance(data, dict):
                logger.error(f"Unexpected response type: {type(data)}")
                raise ValueError("API response is not a dictionary")
                
            if "data" not in data:
                logger.error("Response missing 'data' field")
                logger.error(f"Response keys: {list(data.keys())}")
                raise ValueError("API response missing 'data' field")
                
            if not isinstance(data["data"], list):
                logger.error(f"'data' field is not a list: {type(data['data'])}")
                raise ValueError("API response 'data' field is not a list")
            
            all_transfers.extend(data["data"])
            
            # Handle pagination
            pagination = data.get("pagination", {})
            if pagination:
                logger.debug(f"Pagination info: {json.dumps(pagination, indent=2)}")
            next_page = pagination.get("next_page") if pagination.get("has_more", False) else None
            
            logger.info(f"Retrieved {len(data['data'])} transfers from page {page_count}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response content: {e.response.text}")
            break
        except ValueError as e:
            logger.error(f"Data processing error: {e}")
            if "subscription" in str(e) or "rate limit" in str(e):
                logger.error("Please check your SportMonks API subscription and rate limits")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
            break

    logger.info(f"Total transfers collected: {len(all_transfers)}")
    return all_transfers

def transform_transfer(transfer_data):
    """Transform raw transfer data into the desired format for database storage."""
    try:
        return {
            'transfer_id': transfer_data.get('id'),
            'sport_id': transfer_data.get('sport_id'),
            'player_id': transfer_data.get('player_id'),
            'type_id': transfer_data.get('type_id'),
            'from_team_id': transfer_data.get('from_team_id'),
            'to_team_id': transfer_data.get('to_team_id'),
            'position_id': transfer_data.get('position_id'),
            'detailed_position_id': transfer_data.get('detailed_position_id'),
            'date': transfer_data.get('date'),
            'career_ended': 1 if transfer_data.get('career_ended') else 0,  # Convert boolean to integer for SQLite
            'completed': 1 if transfer_data.get('completed') else 0,  # Convert boolean to integer for SQLite
            'amount': transfer_data.get('amount'),
            'currency': None,  # API doesn't seem to provide currency information
            'player_name': transfer_data.get('player', {}).get('name'),
            'player_common_name': transfer_data.get('player', {}).get('common_name'),
            'from_team_name': transfer_data.get('fromteam', {}).get('name'),
            'from_team_short_code': transfer_data.get('fromteam', {}).get('short_code'),
            'to_team_name': transfer_data.get('toteam', {}).get('name'),
            'to_team_short_code': transfer_data.get('toteam', {}).get('short_code'),
            'processed_at': datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error transforming transfer data: {e}")
        logger.error(f"Raw transfer data: {json.dumps(transfer_data, indent=2)}")
        raise

def load_to_database(conn, transfer):
    """Load transformed transfer into the database."""
    try:
        cursor = conn.cursor()
        
        insert_query = '''
        INSERT OR REPLACE INTO transfers (
            transfer_id, sport_id, player_id, type_id, from_team_id, to_team_id,
            position_id, detailed_position_id, date, career_ended, completed,
            amount, currency, player_name, player_common_name, from_team_name,
            from_team_short_code, to_team_name, to_team_short_code, processed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(insert_query, (
            transfer['transfer_id'],
            transfer['sport_id'],
            transfer['player_id'],
            transfer['type_id'],
            transfer['from_team_id'],
            transfer['to_team_id'],
            transfer['position_id'],
            transfer['detailed_position_id'],
            transfer['date'],
            transfer['career_ended'],
            transfer['completed'],
            transfer['amount'],
            transfer['currency'],
            transfer['player_name'],
            transfer['player_common_name'],
            transfer['from_team_name'],
            transfer['from_team_short_code'],
            transfer['to_team_name'],
            transfer['to_team_short_code'],
            transfer['processed_at']
        ))
        
        conn.commit()
        
    except sqlite3.Error as e:
        logger.error(f"Database insertion error: {e}")
        logger.error(f"Transfer data: {json.dumps(transfer, indent=2)}")
        raise

def get_etl_mode(conn):
    """Get the current ETL mode (historical or incremental)."""
    try:
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS etl_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        conn.commit()
        
        cursor.execute('SELECT value FROM etl_state WHERE key = "etl_mode"')
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # If no mode is stored, start with historical
            cursor.execute('INSERT INTO etl_state (key, value) VALUES (?, ?)', 
                         ("etl_mode", "historical"))
            conn.commit()
            return "historical"
            
    except sqlite3.Error as e:
        logger.error(f"Error getting ETL mode: {e}")
        raise

def update_etl_mode(conn, mode):
    """Update the ETL mode in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO etl_state (key, value) VALUES (?, ?)',
                      ("etl_mode", mode))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating ETL mode: {e}")
        raise

def get_last_processed_date(conn):
    """Get the last processed date from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS etl_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        
        cursor.execute('SELECT value FROM etl_state WHERE key = "last_transfer_date"')
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # If no date is stored, start from 2025-05-01 for historical load
            default_start = "2025-05-01"
            cursor.execute('INSERT INTO etl_state (key, value) VALUES (?, ?)', 
                         ("last_transfer_date", default_start))
            conn.commit()
            return default_start
            
    except sqlite3.Error as e:
        logger.error(f"Error getting last processed date: {e}")
        raise

def update_last_processed_date(conn, date):
    """Update the last processed date in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO etl_state (key, value) VALUES (?, ?)',
                      ("last_transfer_date", date))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating last processed date: {e}")
        raise

def calculate_date_range(start_date_str, is_historical=True):
    """Calculate the date range based on mode."""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    
    if is_historical:
        # For historical loads, process one day at a time
        end_date = start_date
    else:
        # For incremental loads, just get the single day's data
        end_date = start_date
    
    return start_date_str, end_date.strftime("%Y-%m-%d")

def is_caught_up(current_date_str):
    """Check if we've caught up to May 28th, 2025."""
    current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    target_date = datetime.strptime("2025-05-28", "%Y-%m-%d")
    return current_date >= target_date

def main():
    """Main ETL function to process transfers."""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    global sportmonks_key
    sportmonks_key = os.getenv('SPORTMONKS_KEY')
    
    if not sportmonks_key:
        raise ValueError("sportmonks_key not found in environment variables")
    
    # Initialize logging
    global logger
    logger = setup_logging()
    
    logger.info("Starting transfers ETL process")
    
    try:
        # Initialize database
        conn = init_database()
        
        # Get ETL mode and last processed date
        etl_mode = get_etl_mode(conn)
        start_date = get_last_processed_date(conn)
        
        logger.info(f"Running in {etl_mode} mode from {start_date}")
        
        while True:
            # Calculate date range based on mode
            is_historical = etl_mode == "historical"
            start_date, end_date = calculate_date_range(start_date, is_historical)
            
            logger.info(f"Processing transfers from {start_date} to {end_date}")
            
            # Fetch and process transfers
            transfers = fetch_latest_transfers(start_date, end_date)
            logger.info(f"Retrieved {len(transfers)} transfers in total")
            
            successful_transfers = 0
            for transfer in transfers:
                try:
                    transformed_transfer = transform_transfer(transfer)
                    load_to_database(conn, transformed_transfer)
                    successful_transfers += 1
                except Exception as e:
                    logger.error(f"Error processing transfer: {e}")
                    continue
            
            logger.info(f"Successfully processed {successful_transfers} out of {len(transfers)} transfers")
            
            # Calculate next start date
            next_start_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
            
            # Check if we should switch to incremental mode
            if is_historical and is_caught_up(start_date):
                logger.info("🎉 Historical load complete! Switching to incremental mode")
                etl_mode = "incremental"
                update_etl_mode(conn, etl_mode)
                
                # For incremental mode, we want to start from the next day
                update_last_processed_date(conn, next_start_date)
                break
            elif not is_historical:
                # In incremental mode, we process one day and exit
                update_last_processed_date(conn, next_start_date)
                break
            else:
                # In historical mode, continue with next date
                start_date = next_start_date
                update_last_processed_date(conn, start_date)
        
    except Exception as e:
        logger.error(f"Critical error in transfers ETL: {e}", exc_info=True)
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main() 