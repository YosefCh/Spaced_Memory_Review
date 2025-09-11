import subprocess
import pandas as pd
import time
from IPython.display import Markdown, display, clear_output

def run_query(sql_query, display_output=True):
    """
    Simple function to run a SQL query using duck_database_runner.py
    
    Args:
        sql_query (str): The SQL query to execute
        
        display_output (bool): Whether to display the output in a scrollable HTML table. Default is True.
    """
    # Write the query to the SQL file
    with open("sql_query.sql", "w") as f:
        f.write(sql_query)

    # default is to display output. The ai function which uses context data to generate queries uses this function without displaying output
    # as its not necessary to show the user the context data. 
    print("Running query...")
    
    try:
        # must use subprocess as the notebook environment may not support direct execution
        # of the script due to environment constraints
        subprocess.run(['python', 'C:/Users/Rebecca/OneDrive/Documents/Review/Src/duck_database_runner.py'], 
                       check=True, capture_output=True)
        
        # If display_output is False (for ai function), just return after CSV is written
        if not display_output:  
            clear_output(wait=True) 
            # need to print something to clear the "Running query..." message
            print('  ')# Clear the "Running query..." message
            return
        
        # Clear the "Running query..." message and display results
        clear_output(wait=True)
        
        # Read the CSV and display as a nice HTML table with scrolling
        df = pd.read_csv('query_output.csv')
        
        # Create scrollable HTML table
        html_table = df.to_html(escape=False, table_id="query_results")
        
        # Add CSS for scrolling and better formatting (works in both light and dark mode)
        scrollable_html = f"""
        <style>
        #query_results {{
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid rgb(110, 140, 210);
            font-family: monospace;
            background-color: rgb(220, 230, 220);
            color: black;
        }}
        #query_results th {{
            background-color: rgb(100, 100, 100);
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
            font-weight: bold;
        }}
        #query_results td, #query_results th {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid var(--jp-border-color2, #ccc);
        }}
        
        #query_results tr:nth-child(even) {{
            background-color: rgb(220, 255, 255);
        }}
        </style>
        <div>
        <h4>Query Results ({len(df)} rows)</h4>
        {html_table}
        </div>
        """
        
        from IPython.display import HTML
        display(HTML(scrollable_html))
        
    except subprocess.CalledProcessError as e:
        clear_output(wait=True)
        with open('sql_error_message.txt', 'r') as f:    
            error = f.read()
            display(Markdown(error))
