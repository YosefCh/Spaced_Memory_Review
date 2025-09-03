def all_data():
    return "SELECT * FROM learned_material;"

def count_subjects():
    return """SELECT 
    COALESCE(Subject, 'Skipped') AS Subject,
    COUNT(*) AS count
    FROM learned_material
    GROUP BY Subject
    ORDER BY Count DESC;"""
    
def count_topics():
    return """SELECT 
    COALESCE(Topic, 'Skipped') AS Topic,
    COUNT(*) AS count
    FROM learned_material
    GROUP BY Topic
    ORDER BY Count DESC;"""
    

def skipped_days():
    return """SELECT 
    Index Day_Number, Date
    FROM learned_material 
    WHERE FilePath IS NULL OR FilePath = ''
    ORDER BY Date;"""

def unique_subjects():
    return """SELECT DISTINCT Subject 
    FROM learned_material 
    WHERE Subject IS NOT NULL AND Subject != ''
    ORDER BY Subject;"""
    
def unique_topics():
    return """SELECT DISTINCT Topic 
    FROM learned_material 
    WHERE Topic IS NOT NULL AND Topic != ''
    ORDER BY Topic;"""


def learning_streak():
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


def total_learning_days():
    return """SELECT 
    COUNT(*) as total_days_learned
    FROM learned_material 
    WHERE FilePath IS NOT NULL;"""

