

# AI_text_to_query_converter.py
def natural_language_to_query(natural_language):
    
    # necessary if the output query is to be displayed to the user
    # from IPython.display import Markdown, display
    from IPython.display import display, clear_output, Markdown
    from AI_class import OpenAIClient
    import query_runner
    import time
    a = OpenAIClient()
    
    
    display(Markdown(f"**Your question:** {natural_language}"))
    print('Fetching context data from the database...\n')
    time.sleep(1)
    clear_output(wait=True)
    
    # Get distinct subjects and topics for context to feed the model but do not display it to the user 
    query_runner.run_query("select distinct subject, topic, Date FROM learned_material where subject is not null;", display_output=False)
    with open('query_output.csv', 'r') as f:
        data = f.read()

    context = f"""I have a spaced memory reiview program/app where users submit material or have an AI generate material for me to learn and review over time. 
    My progran writes the material to a duckdb database and I have a query tool using real sql queries to understand my data better.
    I want you to help me generate SQL queries for users who are non-technical and do not know SQL. They will submit a question about the data in natural
    language and you will generate the SQL query for them to use in my app. 

    Keep in mind that users might not use the correct names for the columns they 
    would like to query. You will need to interpret what they mean and map it to the correct column name.

    Additionally, if they say "give me all the material i need for science subjects", you will need to include in the query all the names 
    of the subjects that are considered science subjects. This includes but is not limited to: Physics, Chemistry, Biology, Earth Science, Astronomy, Environmental Science, 
    and any other subject that is commonly recognized as a science discipline.The same can be said for other general subjects like Math, History, etc.
    Sometimes, users will request material and the query might need to include the subject and topic column to find the relevant material.

    Please respond only with the SQL query and nothing else. Do not even include backticks: ```.
    The database is called 'learned_material' and the columns are as follows:

    - Index, (have not really used it much in my queries)
    - Date,   (the day the material was created). When querying the duckdb database, here is an example of how you can filter by date:
                SQL:
                select * from learned_material where
                Date BETWEEN CURRENT_DATE - INTERVAL '2 months' AND CURRENT_DATE
                          
    - FilePath, (the full path where the material is stored on my computer as an html file. This contains the name of file)
    - Subject,  (The general subject of learning, such as Python, Math, History, etc.)
    - Topic      (The specific topic of the material, such as Python Lists, Math Derivatives, History WW2, etc.)

    REFERENCE DATA (for context only - do not output this):
    Available subjects and topics in the database include: {data}


    The database contains placeholders for thousands of rows of data and most of the time there will be plenty of empty rows for the dates in the future.
    Additionally, on days that the user did not submit data, the database will only have values for the index and date columns.

    Two additional points to keep in mind:
    1. The filepaths are long, so if the users request includes the filepahts, configure the query to have the filepaths column as the last column in the query results.
    2. As the user will be using natural language, the preference for an "ORDER BY" will not necessarily be explicitly stated. Therefore, use the "ORDER BY" clause in a way we can assume the user would want it.
    3. If the user requests someting unrelated to the database or something incoherent, respond with "I am sorry, but I cannot assist with that request."
    """
    
    print("Generating query...\n")
    clear_output(wait=True)
    z = a.get_response(f"""Given this context: {context}
                                    Here is the natural language question from the user:
                                    {natural_language}
                                    """)

    # optional to see the query generated
    #display(Markdown(f"__Your question:__ {natural_language}"))
    print(f"Generated SQL query: '\n'")
    display(Markdown(f"```sql\n{z}\n```"))

    return query_runner.run_query(z)
        