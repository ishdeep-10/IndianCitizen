import schedule
import time
from twitter_etl import run_etl_pipeline
import os
from dotenv import load_dotenv

def job():
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': os.getenv("MAINNET_API_KEY")  
    }

    MAINNET_API_URL = os.getenv("MAINNET_API_URL")
    url = f'{MAINNET_API_URL}/api/v1/on_demand_data_request'
    
    target_accounts = [

        "@webuildscore",
        "@thedkingdao"
    ]

    # Initial start date for historical data
    start_date = "2025-05-01T00:00:00Z"
    
    run_etl_pipeline(url, headers, start_date, target_accounts)

def main():
    load_dotenv()
    
    # Run immediately on start
    job()
    
    # Schedule to run every day on 12:00
    schedule.every().day.at("12:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 