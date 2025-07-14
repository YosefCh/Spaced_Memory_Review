import duckdb
import pandas as pd
import re

INPUT_SQL_PATH = 'sql_query.sql'
OUTPUT_CSV_PATH = 'query_output.csv'
CSV_SOURCE_PATH = 'C:/Users/Rebecca/OneDrive/Documents/Review/Data/learned_material.csv'

def main():
    # Read the SQL query
    with open(INPUT_SQL_PATH, 'r') as f:
        user_sql = f.read()

    # Open DuckDB connection
    con = duckdb.connect()

    # Read CSV and do simple cleaning
    df = pd.read_csv(CSV_SOURCE_PATH)
    
    # Simple cleaning: filter nulls and clean spaces
    df = df[df['Subject'].notna()]  # Remove nulls
    df = df[df['Subject'].str.strip() != '']  # Remove empty strings
    df['Subject'] = df['Subject'].str.strip()  # Remove leading/trailing spaces
    df['Subject'] = df['Subject'].str.replace(r'\s+', ' ', regex=True)  # Fix multiple spaces
    
    # Also clean Topic column
    df = df[df['Topic'].notna()]  # Remove nulls
    df = df[df['Topic'].str.strip() != '']  # Remove empty strings
    df['Topic'] = df['Topic'].str.strip()  # Remove leading/trailing spaces
    df['Topic'] = df['Topic'].str.replace(r'\s+', ' ', regex=True)  # Fix multiple spaces
    

    
    # Create the view in DuckDB
    con.execute("CREATE OR REPLACE VIEW learned_material AS SELECT * FROM df")

    # Run the query
    print("Running query...")
    result_df = con.execute(user_sql).fetchdf()

    # Save result
    result_df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Query complete. Output written to {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    main()
