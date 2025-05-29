import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from typing import List, Dict

def create_database():
    """
    Creates the SQLite database and transfer_rumours table if they don't exist.
    """
    conn = sqlite3.connect('sportmonks.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transfer_rumours (
        player_name TEXT,
        position TEXT,
        age INTEGER,
        current_club TEXT,
        interested_club TEXT,
        contract_expiry_date TEXT,
        market_value TEXT,
        probability INTEGER,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def safe_int_convert(value: str, default: int = 0) -> int:
    """
    Safely converts a string to integer, returning default value if conversion fails.
    """
    try:
        # Remove any non-numeric characters
        cleaned_value = ''.join(c for c in value if c.isdigit())
        return int(cleaned_value) if cleaned_value else default
    except (ValueError, AttributeError):
        return default

def clean_text(text: str) -> str:
    """
    Cleans text by removing extra whitespace and newlines.
    """
    if not text:
        return 'N/A'
    return ' '.join(text.strip().split())

def safe_get_text(element, default='N/A'):
    """
    Safely gets text from an element, returning default if element is None.
    Also handles cases where the element exists but has no text.
    """
    if element is None:
        return default
    try:
        text = element.get_text(strip=True)
        return clean_text(text) if text else default
    except (AttributeError, TypeError):
        return default

def get_transfer_rumors() -> List[Dict]:
    """
    Scrapes transfer rumors from Transfermarkt website (premium version).
    Returns a list of dictionaries containing rumor details.
    """
    base_url = "https://www.transfermarkt.com/geruechte/topgeruechte/statistik"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
    }

    all_rumors = []
    page = 1
    
    while True:
        try:
            # Construct URL with page parameter
            url = f"{base_url}?plus=1&page={page}"
            print(f"\nScraping page {page}...")
            
            time.sleep(2)  # Respectful delay between requests
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'class': 'items'})
            if not table:
                print(f"No more data found on page {page}. Stopping pagination.")
                break

            # Check if there are any rows in this page
            rows = table.find_all('tr', {'class': ['odd', 'even']})
            if not rows:
                print(f"No rows found on page {page}. Stopping pagination.")
                break

            for row in rows:
                try:
                    # Get only direct child td elements
                    columns = row.find_all('td', recursive=False)
                    if len(columns) < 8:  # We need at least 8 columns
                        print(f"Skipping row: insufficient columns (found {len(columns)}, need 8)")
                        continue

                    try:
                        # Player name and position from first column's nested table
                        player_cell = columns[0]
                        inline_table = player_cell.find('table', {'class': 'inline-table'})
                        if not inline_table:
                            print("Could not find inline table for player info")
                            continue

                        # Player name is in the first row's hauptlink cell
                        player_link = inline_table.find('td', {'class': 'hauptlink'}).find('a')
                        player_name = safe_get_text(player_link)
                        
                        # Position is in the second row's td
                        table_rows = inline_table.find_all('tr')
                        if len(table_rows) > 1:
                            position_td = table_rows[1].find('td')
                            position = safe_get_text(position_td) if position_td else 'N/A'
                        else:
                            position = 'N/A'
                        
                        # Age from second column - handle nested font elements
                        age_cell = columns[1]
                        # Try to get text from innermost font element first
                        age_text = None
                        font_elements = age_cell.find_all('font')
                        if font_elements:
                            # Get the innermost font element's text
                            age_text = safe_get_text(font_elements[-1])
                        if not age_text:
                            # Fallback to direct cell text if no font elements
                            age_text = safe_get_text(age_cell)
                        age = safe_int_convert(age_text)
                        
                        # Current club from fourth column (index 3)
                        current_club_cell = columns[3]
                        current_club_table = current_club_cell.find('table', {'class': 'inline-table'})
                        if current_club_table:
                            current_club_link = current_club_table.find('td', {'class': 'hauptlink'}).find('a')
                            current_club = safe_get_text(current_club_link)
                        else:
                            current_club = 'N/A'
                        
                        # Interested club from fifth column (index 4)
                        interested_club_cell = columns[4]
                        interested_club_table = interested_club_cell.find('table', {'class': 'inline-table'})
                        if interested_club_table:
                            interested_club_link = interested_club_table.find('td', {'class': 'hauptlink'}).find('a')
                            interested_club = safe_get_text(interested_club_link)
                        else:
                            interested_club = 'N/A'
                        
                        # Contract expiry from sixth column (index 5)
                        contract_cell = columns[5]
                        font_elements = contract_cell.find_all('font')
                        contract_expiry = safe_get_text(font_elements[-1]) if font_elements else safe_get_text(contract_cell)
                        
                        # Market value from seventh column (index 6)
                        market_cell = columns[6]
                        font_elements = market_cell.find_all('font')
                        market_value = safe_get_text(font_elements[-1]) if font_elements else safe_get_text(market_cell)
                        
                        # Probability from eighth column (index 7)
                        prob_cell = columns[7]
                        font_elements = prob_cell.find_all('font')
                        probability_text = safe_get_text(font_elements[-1], '0') if font_elements else safe_get_text(prob_cell, '0')
                        probability = safe_int_convert(probability_text.split('%')[0])  # Get just the number

                        rumor = {
                            'player_name': player_name,
                            'position': position,
                            'age': age,
                            'current_club': current_club,
                            'interested_club': interested_club,
                            'contract_expiry_date': contract_expiry,
                            'market_value': market_value,
                            'probability': probability
                        }
                        all_rumors.append(rumor)
                        
                        # Debug print with more detail
                        print(f"Successfully processed row:")
                        print(f"  Player: {player_name}")
                        print(f"  Position: {position}")
                        print(f"  Age: {age}")
                        print(f"  Current Club: {current_club}")
                        print(f"  Interested Club: {interested_club}")
                        print(f"  Contract: {contract_expiry}")
                        print(f"  Market Value: {market_value}")
                        print(f"  Probability: {probability}%")
                        print("-" * 50)
                        
                    except (AttributeError, TypeError) as e:
                        print(f"Error extracting data from row: {str(e)}")
                        print("Row HTML:")
                        print(row.prettify())
                        continue

                except Exception as e:
                    print(f"Unexpected error processing row: {str(e)}")
                    print("Row HTML:")
                    print(row.prettify())
                    continue

            # Check if there's a next page by looking for pagination
            pagination = soup.find('div', {'class': 'pager'})
            if not pagination or f'page={page + 1}' not in str(pagination):
                print(f"No more pages found after page {page}. Stopping pagination.")
                break

            page += 1

        except requests.RequestException as e:
            print(f"Error fetching data for page {page}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            break

    print(f"\nTotal rumors collected: {len(all_rumors)}")
    return all_rumors

def save_to_database(rumors: List[Dict]):
    """
    Saves the scraped rumors to the SQLite database.
    """
    if not rumors:
        print("No data to save")
        return
        
    conn = sqlite3.connect('sportmonks.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM transfer_rumours')
    
    # Insert new data
    for rumor in rumors:
        cursor.execute('''
        INSERT INTO transfer_rumours (
            player_name,position, age, current_club, interested_club,
            contract_expiry_date, market_value, probability
        ) VALUES (?,?, ?, ?, ?, ?, ?, ?)
        ''', (
            rumor['player_name'],
            rumor['position'],
            rumor['age'],
            rumor['current_club'],
            rumor['interested_club'],
            rumor['contract_expiry_date'],
            rumor['market_value'],
            rumor['probability']
        ))
    
    conn.commit()
    print(f"Saved {len(rumors)} rumors to database")
    
    # Display first few entries
    cursor.execute('SELECT * FROM transfer_rumours LIMIT 5')
    rows = cursor.fetchall()
    print("\nFirst few entries in database:")
    for row in rows:
        print(row)
    
    conn.close()

if __name__ == "__main__":
    print("Setting up database...")
    create_database()
    
    print("Scraping transfer rumors...")
    rumors = get_transfer_rumors()
    
    if rumors:
        print(f"\nFound {len(rumors)} transfer rumors")
        save_to_database(rumors)
    else:
        print("No rumors found or error occurred") 