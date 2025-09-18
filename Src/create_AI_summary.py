from AI_text_to_query_converter import natural_language_to_query
from AI_class import OpenAIClient
from IPython.display import display, Markdown, clear_output
import time
import pandas as pd
import os

class AISummaryTool:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.query_output_file = os.path.join(self.BASE_DIR, "query_output.csv")
        

    def find_files(self):
        display(Markdown("**Please enter which material you want to summarize:**"))
        question = input("Your question: ")
        time.sleep(1)
        natural_language_to_query(question, display_output=False, purpose="summary")
        
        df = pd.read_csv(self.query_output_file)
        files = df['FilePath'].dropna().tolist()
        subjects = df['Subject'].dropna().tolist()
        topics = df['Topic'].dropna().tolist()
        return files, subjects, topics

    def extract_material(self):
        files, subjects, topics = self.find_files()
        material_content = ""
        for i in files:
            with open(i, 'r', encoding='utf-8') as file:
                content = file.read()
                section_start = content.find('<div id="text">')
                section_end = content.find('</div><br>', section_start)
                section_content = content[section_start:section_end]
                material_content += f"\n\n### Subject: {subjects[files.index(i)]}\n"
                material_content += f"### Topic: {topics[files.index(i)]}\n"
                material_content += section_content
        
        return material_content
    
    