import duckdb
import pandas as pd
import sys
from IPython.display import Markdown, HTML, display
from datetime import datetime

INPUT_SQL_PATH = 'sql_query.sql'
OUTPUT_CSV_PATH = 'query_output.csv'
CSV_SOURCE_PATH = 'C:/Users/Rebecca/OneDrive/Documents/Review/Data/learned_material.csv'

def main():
    # Read the SQL query
    with open(INPUT_SQL_PATH, 'r') as f:
        user_sql = f.read()

    # Open DuckDB connection
    con = duckdb.connect()

    # Read CSV and filter by date only
    df = pd.read_csv(CSV_SOURCE_PATH)
    
    # Convert Date column to datetime for comparison
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Filter to only include dates from 4/21/2025 up to today
    start_date = datetime(2025, 4, 21)
    today = datetime.now()
    df = df[(df['Date'] >= start_date) & (df['Date'] <= today)]
    
    # Clean Subject col from leading and trailing white spaces (but only non null values as null should be kept for record keeping)
    df.loc[df['Subject'].notna(), 'Subject'] = df.loc[df['Subject'].notna(), 'Subject'].str.strip()
    
    # Replace multiple spaces between words with a single space. Crucial for filtering and grouping consistently.
    df.loc[df['Subject'].notna(), 'Subject'] = df.loc[df['Subject'].notna(), 'Subject'].str.replace(r'\s+', ' ', regex=True)
    # same for the Topic column
    df.loc[df['Topic'].notna(), 'Topic'] = df.loc[df['Topic'].notna(), 'Topic'].str.strip()
    df.loc[df['Topic'].notna(), 'Topic'] = df.loc[df['Topic'].notna(), 'Topic'].str.replace(r'\s+', ' ', regex=True)
    
    # Convert Date back to string format for DuckDB compatibility
    #df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    

    
    # Create the view in DuckDB
    con.execute("CREATE OR REPLACE VIEW learned_material AS SELECT * FROM df")

    try:
        # Run the query
        print("Running query...")
        result_df = con.execute(user_sql).fetchdf()
        
        # Clear any previous error messages on successful execution
        with open('sql_error_message.txt', 'w') as f:
            f.write("")
        
        # Save result
        result_df.to_csv(OUTPUT_CSV_PATH, index=False)
        with open(OUTPUT_CSV_PATH, 'r') as f:
            print(f"Query output saved to {OUTPUT_CSV_PATH}:\n{f.read()}")
    except Exception as e:
        with open('sql_error_message.txt', 'w') as f:
            f.write(f"Error occurred:\n{e}\n")
        sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    main()
