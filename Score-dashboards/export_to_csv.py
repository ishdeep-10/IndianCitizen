import sqlite3
import pandas as pd

def export_data():
    """
    Export data from SQLite to CSV for cloud deployment
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('sportmonks.db')
        
        # Read data
        query = "SELECT * FROM transfer_rumours"
        df = pd.read_sql_query(query, conn)
        
        # Export to CSV
        df.to_csv('transfer_rumours.csv', index=False)
        print("Data successfully exported to transfer_rumours.csv")
        
    except Exception as e:
        print(f"Error exporting data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_data() 