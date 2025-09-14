from IPython.display import Markdown, display

class StandardQueries:
    def __init__(self):
        self.queries = {
            1: ("All Data", self._all_data),
            2: ("Count Subjects", self._count_subjects),
            3: ("Count Topics", self._count_topics),
            4: ("Skipped Days", self._skipped_days),
            5: ("Unique Subjects", self._unique_subjects),
            6: ("Unique Topics", self._unique_topics),
            7: ("Learning Streak", self._learning_streak),
            8: ("Total Learning Days", self._total_learning_days)
        }
    
    def _all_data(self):
        return "SELECT * FROM learned_material;"

    def _count_subjects(self):
        return """SELECT 
        COALESCE(Subject, 'Skipped') AS Subject,
        COUNT(*) AS count
        FROM learned_material
        GROUP BY Subject
        ORDER BY Count DESC;"""
        
    def _count_topics(self):
        return """SELECT 
        COALESCE(Topic, 'Skipped') AS Topic,
        COUNT(*) AS count
        FROM learned_material
        GROUP BY Topic
        ORDER BY Count DESC;"""
        
    def _skipped_days(self):
        return """SELECT 
        Index Day_Number, Date
        FROM learned_material 
        WHERE FilePath IS NULL OR FilePath = ''
        ORDER BY Date;"""

    def _unique_subjects(self):
        return """SELECT DISTINCT Subject 
        FROM learned_material 
        WHERE Subject IS NOT NULL AND Subject != ''
        ORDER BY Subject;"""
        
    def _unique_topics(self):
        return """SELECT DISTINCT Topic 
        FROM learned_material 
        WHERE Topic IS NOT NULL AND Topic != ''
        ORDER BY Topic;"""

    def _learning_streak(self):
        return """
        WITH streak_ends AS (
            select 0 as streak_end
            UNION all
            select "Index" as streak_end from learned_material
            WHERE FilePath IS NULL OR FilePath = ''
            UNION all
            select (SELECT MAX("Index") FROM learned_material) + 1 as streak_end
        ),
        streak_lengths AS (
            select 
                streak_end - LAG(streak_end, 1, 0) OVER (ORDER BY streak_end) - 1 as streak_length,
                LAG(streak_end, 1, 0) OVER (ORDER BY streak_end) + 1 as streak_start,
                streak_end - 1 as streak_end_day
            from streak_ends
            WHERE streak_end > 0
        )
        SELECT 
            streak_length as longest_streak_days,
            streak_start as streak_start_day,
            streak_end_day
        FROM streak_lengths
        WHERE streak_length = (SELECT MAX(streak_length) FROM streak_lengths)
        AND streak_length > 0;"""

    def _total_learning_days(self):
        return """SELECT 
        COUNT(*) as total_days_learned
        FROM learned_material 
        WHERE FilePath IS NOT NULL;"""
    
    def display_menu(self):
        menu_markdown = "## 📊 Available Queries\n\n"
        
        for num, (description, _) in self.queries.items():
            menu_markdown += f"**{num}.** {description}\n\n"
        
        menu_markdown += "---"
        
        display(Markdown(menu_markdown))
    
    def get_user_choice(self):
        min_choice = min(self.queries.keys())
        max_choice = max(self.queries.keys())
        
        while True:
            try:
                choice = int(input(f"Enter a number ({min_choice}-{max_choice}): "))
                if choice in self.queries:
                    return choice
                else:
                    display(Markdown(f"❌ **Invalid choice!** Please enter a number between {min_choice} and {max_choice}."))
            except ValueError:
                display(Markdown(f"⚠️ **Invalid input!** Please enter a number between {min_choice} and {max_choice}."))
    
    def get_query(self, query_number):
        if query_number in self.queries:
            return self.queries[query_number][1]()
        else:
            raise ValueError(f"Query number {query_number} not found!")
    
    def run_interactive(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            query = self.get_query(choice)
            
            return query
            
            

Standard_Query = StandardQueries()