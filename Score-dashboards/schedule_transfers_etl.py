import schedule
import time
from transfers_etl import main as job
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    # Run immediately on start
    job()
    
    # Schedule to run every day at 12:00
    schedule.every().day.at("12:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 