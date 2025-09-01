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
    Date
    FROM learned_material 
    WHERE FilePath IS NULL OR FilePath = ''
    ORDER BY Date;"""

def unique_subjects():
    return """SELECT DISTINCT Subject 
    FROM learned_material 
    WHERE Subject IS NOT NULL AND Subject != ''
    ORDER BY Subject;"""




def learning_streak():
    return """SELECT 
    COUNT(*) as consecutive_days
    FROM learned_material 
    WHERE FilePath IS NOT NULL 
    AND Date >= (
        SELECT MIN(Date) 
        FROM learned_material 
        WHERE Date <= CURRENT_DATE 
        AND FilePath IS NULL
    );"""


def total_learning_days():
    return """SELECT 
    COUNT(*) as total_days_learned
    FROM learned_material 
    WHERE FilePath IS NOT NULL;"""

def entries_by_month():
    return """SELECT 
    strftime('%Y-%m', Date) as month,
    COUNT(*) as entries
    FROM learned_material 
    WHERE FilePath IS NOT NULL
    GROUP BY strftime('%Y-%m', Date)
    ORDER BY month;"""