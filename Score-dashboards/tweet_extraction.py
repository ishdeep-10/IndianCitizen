import pandas as pd
import json
import os
from utils import *

headers = {
    'Content-Type': 'application/json',
    # The server uses `verify_api_key` Depends, so we should pass it as a header
    'X-API-KEY': os.getenv("MAINNET_API_KEY")  
}

MAINNET_API_URL = os.getenv("MAINNET_API_URL")
url = f'{MAINNET_API_URL}/api/v1/on_demand_data_request'


data = {
    "source": "x",  # Based on DataSource enum in the code
    "usernames": ["@webuildscore","@thedkingdao"],
    "limit": 1000,  # Default is 100, max is 1000
    "start_date": "2025-05-20T00:00:00Z" # Datetime should be in ISO format
}

result = get_data(url, headers, data)
