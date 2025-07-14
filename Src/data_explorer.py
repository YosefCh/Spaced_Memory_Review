import json
import duckdb
import pandas as pd

CSV_SOURCE_PATH = 'C:/Users/Rebecca/OneDrive/Documents/Review/Data/learned_material.csv'
QUERIES_PATH = 'predefined_queries.json'
OUTPUT_CSV_PATH = 'query_output.csv'

class DataExplorer:
    """
    User-friendly data exploration tool for learning analytics.
    Allows users to explore their learning data without writing SQL.
    """
    
    def __init__(self):
        self.queries = self.load_queries()
        self.df = None
        self.con = None
        
    def load_queries(self):
        """Load predefined queries from JSON file."""
        with open(QUERIES_PATH, 'r') as f:
            return json.load(f)['queries']
    
    def setup_database(self):
        """Set up DuckDB connection and clean data."""
        # Read and clean the data (same logic as duck_database_runner.py)
        self.df = pd.read_csv(CSV_SOURCE_PATH)
        # print(self.df.head())
        
        # Simple cleaning: filter nulls and clean spaces
        self.df = self.df[self.df['Subject'].notna()]
        self.df = self.df[self.df['Subject'].str.strip() != '']
        self.df['Subject'] = self.df['Subject'].str.strip()
        self.df['Subject'] = self.df['Subject'].str.replace(r'\s+', ' ', regex=True)
        
        # Also clean Topic column
        self.df = self.df[self.df['Topic'].notna()]
        self.df = self.df[self.df['Topic'].str.strip() != '']
        self.df['Topic'] = self.df['Topic'].str.strip()
        self.df['Topic'] = self.df['Topic'].str.replace(r'\s+', ' ', regex=True)
        
        
        # Create DuckDB connection and view
        self.con = duckdb.connect()
        # Register the DataFrame as a table that can be queried
        self.con.register('learned_material', self.df)
    
    def show_menu(self):
        """Display the menu of available queries."""
        print("🔍 Explore Your Learning Data")
        print("=" * 40)
        print("What would you like to know about your learning?")
        print()
        
        for query_id, query_info in self.queries.items():
            print(f"{query_info['number']}. {query_info['name']}")
            print(f"   📝 {query_info['description']}")
            print()
        
        print("0. Exit")
        print("=" * 40)
    
    def get_user_choice(self):
        """Get user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (0-7): ").strip()
                if choice == "0":
                    return 0
                elif choice in self.queries:
                    return int(choice)
                else:
                    print("❌ Invalid choice. Please enter a number from 0-7.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def execute_query(self, query_id):
        """Execute the selected query and display results."""
        query_info = self.queries[str(query_id)]
        sql_query = query_info['sql']
        
        print(f"🔍 {query_info['name']}")
        print(f"📝 {query_info['description']}")
        print()
        
        try:
            # Execute query
            result_df = self.con.execute(sql_query).fetchdf()
            
            # Display results
            if len(result_df) == 0:
                print("📭 No data found for this query.")
            else:
                print("📊 Results:")
                print(result_df.to_string(index=False))
                
                # Save to CSV
                result_df.to_csv(OUTPUT_CSV_PATH, index=False)
                print(f"\n💾 Results saved to {OUTPUT_CSV_PATH}")
                
        except Exception as e:
            print(f"❌ Error executing query: {e}")
        
        print("\n" + "=" * 50 + "\n")
    
    def run(self):
        """Main interface loop."""
        print("🚀 Setting up database...")
        self.setup_database()
        print("✅ Database ready!")
        print()
        
        while True:
            self.show_menu()
            choice = self.get_user_choice()
            
            if choice == 0:
                print("👋 Thanks for exploring your learning data!")
                break
            else:
                self.execute_query(choice)

def main():
    """Entry point for the data explorer."""
    explorer = DataExplorer()
    explorer.run()

if __name__ == "__main__":
    main()
