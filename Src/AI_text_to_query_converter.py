
# AI_text_to_query_converter.py
def natural_language_to_query(natural_language, display_output=True, purpose="query"):
    
    # purpose param is necessary if the output query is to be displayed to the user

    from IPython.display import display, clear_output, Markdown
    from AI_class import OpenAIClient, Reasoning_OpenAIClient
    import query_runner
    import time
    import os
    
    
    ai = Reasoning_OpenAIClient()
    backup_ai = OpenAIClient(model_name="gpt-4.1-mini")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    query_output_file = os.path.join(BASE_DIR, "query_output.csv")
    display(Markdown(f"**Your entered:** {natural_language}"))
    print('Fetching context data from the database...\n')
    time.sleep(1)
    clear_output(wait=True)
    
    # Get distinct subjects and topics for context to feed the model but do not display it to the user 
    query_runner.run_query("select distinct subject, topic, Date FROM learned_material where subject is not null;", display_output=False)
    with open(query_output_file, 'r') as f:
        data = f.read()

    if purpose == "summary":
        context = f"""I have a spaced memory review program/app where users submit material or have an AI generate material for them to learn and review over time. 
        My program writes the material to a duckdb database and has a query tool using real sql queries to help better understand the data.
        I want you to help me generate SQL queries for users who are non-technical and do not know SQL. They will submit a question about the data in natural
        language and you will generate the SQL query for them to use in my app.
        
        IMPORTANT: This request is for CONTENT SUMMARIZATION purposes. The user wants to identify individual files/records to read and summarize their content.
        
        CRITICAL RULES FOR SUMMARY QUERIES:
        1. NEVER use aggregation functions (COUNT, SUM, GROUP BY, HAVING, etc.)
        2. ALWAYS return individual records, not grouped or counted data
        3. The goal is to get a list of specific files/materials to read and summarize
        4. When user says "summarize", "give me a summary", or similar - they want the INDIVIDUAL RECORDS that contain the material to be summarized
        5. Focus on SELECT statements that return individual rows of data
        6. ALWAYS include FilePath in the SELECT clause as this is needed to read the files
        7. Include Subject and Topic to help identify what each file contains
        8. Use WHERE clauses to filter for the specific material they want
        
        SELECT FORMAT for summaries: SELECT Subject, Topic, FilePath FROM learned_material WHERE [conditions]
        
        Example interpretations:
        - "Summarize my math topics" → SELECT Subject, Topic, FilePath FROM learned_material WHERE Subject ILIKE '%math%'
        - "Give me a summary of physics from last month" → SELECT Subject, Topic, FilePath FROM learned_material WHERE Subject ILIKE '%physics%' AND Date >= CURRENT_DATE - INTERVAL '1 month'
        - "Summarize everything I learned about programming" → SELECT Subject, Topic, FilePath FROM learned_material WHERE Subject ILIKE '%programming%' OR Topic ILIKE '%programming%'
        
        The database is called 'learned_material' and the columns are as follows:
        - Index, (have not really used it much in queries)
        - Date, (the day the material was created). When querying the duckdb database, here is an example of how you can filter by date:
                    SQL: select * from learned_material where Date BETWEEN CURRENT_DATE - INTERVAL '2 months' AND CURRENT_DATE
        - FilePath, (the full path where the material is stored on my computer as an html file. This contains the name of file)
        - Subject, (The general subject of learning, such as Python, Math, History, etc.)
        - Topic (The specific topic of the material, such as Python Lists, Math Derivatives, History WW2, etc.)
        
        Keep in mind that users might not use the correct names for the columns they would like to query. 
        You will need to interpret what they mean and map it to the correct column name.
        
        Additionally, if they say "give me all the material about science subjects", you will need to include in the query all the names 
        of the subjects that are considered science subjects. This includes but is not limited to: Physics, Chemistry, Biology, Earth Science, Astronomy, Environmental Science, 
        and any other subject that is commonly recognized as a science discipline. 
        Another example; if the user wants all material for machine learning classification algorithms, don't simply filter for "machine learning" the subject and "classification" the topic.
        Rather, include all relevant topics like "decision trees", "random forests", "support vector machines", "logistic regression", "k-nearest neighbors", etc.
        The same can be said for other general subjects like Math, History, etc. As you should use your own knowledge of subject matter in additon,
        to how a typical user would query the database.
        
        The database contains placeholders for thousands of rows of data and most of the time there will be plenty of empty rows for the dates in the future.
        Additionally, on days that the user did not submit data, the database will only have values for the index and date columns.
        
        Additional points to keep in mind:
        1. Always put FilePath as the last column in the SELECT clause since filepaths are long
        2. Use ORDER BY in a logical way (usually by Date or Subject)
        3. If the user requests something unrelated to the database or something incoherent, respond with "Invalid Query."
        4. Remember: NO AGGREGATIONS - we want individual records to read and summarize
        
        REFERENCE DATA (for context only - do not output this):
        Available subjects and topics in the database include: {data}
        
        Please respond only with the SQL query and nothing else. Do not include backticks: ```.
        """
    else:
        context = f"""I have a spaced memory review program/app where users submit material or have an AI generate material for them to learn and review over time. 
        My program writes the material to a duckdb database and I have a query tool using real sql queries to help better understand the data.
        I want you to help me generate SQL queries for users who are non-technical and do not know SQL. They will submit a question about the data in natural
        language and you will generate the SQL query for them to use in my app. 

        Keep in mind that users might not use the correct names for the columns they 
        would like to query. You will need to interpret what they mean and map it to the correct column name.

        Additionally, if they say "give me all the material about science subjects", you will need to include in the query all the names 
        of the subjects that are considered science subjects. This includes but is not limited to: Physics, Chemistry, Biology, Earth Science, Astronomy, Environmental Science, 
        and any other subject that is commonly recognized as a science discipline. 
        Another example; if the user wants all material for machine learning classification algorithms, don't simply filter for "machine learning" the subject and "classification" the topic.
        Rather, include all relevant topics like "decision trees", "random forests", "support vector machines", "logistic regression", "k-nearest neighbors", etc.
        The same can be said for other general subjects like Math, History, etc. As you should use your own knowledge of subject matter in additon,
        to how a typical user would query the database.

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
        1. The filepaths are long, so if the users request includes the filepaths, configure the query to have the filepaths column as the last column in the query results.
        2. As the user will be using natural language, the preference for an "ORDER BY" will not necessarily be explicitly stated. Therefore, use the "ORDER BY" clause in a way we can assume the user would want it.
        3. If the user requests something unrelated to the database or something incoherent, respond with "Invalid Query."
        """
    
    print("Generating query...\n")
    clear_output(wait=True)
    z = ai.get_response(f"""Given this context: {context}
                                    Here is the natural language question from the user:
                                    {natural_language}
                                    """)
    
    if z.startswith("An error occurred"):
        z = backup_ai.get_response(f"""Given this context: {context}
                                    Here is the natural language question from the user:
                                    {natural_language}
                                    """)
    # optional to see the query generated
    #display(Markdown(f"__Your question:__ {natural_language}"))
    if z == "Invalid Query.":
        error_message = "### **The system was unable to generate a valid SQL query based on your input.**\n\nPlease try rephrasing your question or providing more specific details about the data you are looking for."
        display(Markdown(error_message))
        return
    print(f"Generated SQL query: \n")
    display(Markdown(f"```sql\n{z}\n```"))
    
    time.sleep(1)
    # when display output is false we must clear output here as it we don't have it done for us in the query_runner function
    clear_output(wait=True)

    if display_output:
        return query_runner.run_query(z)
    else:
        return query_runner.run_query(z, display_output=False)