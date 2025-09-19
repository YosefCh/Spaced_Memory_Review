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
    
    def generate_summary(self):
        material_content = self.extract_material()
        ai = OpenAIClient(system_role_content="You are an expert at summarizing educational material.")
        prompt = f"""Please provide a concise summary of the following material:\n\n{material_content}\n\n:
                     Summarize the key points and main ideas in a clear and organized manner.
                     Each subject and topic should be clearly labeled in the summary. They should also be bolded.
                     IMPORTANT: THE EXACT CONTENT SHOULD BE SUMMARIZED EVEN IF YOU THINK IT IS NOT NECESSARILY THE TYPICAL WAY OF PRESENTING
                     THE INFORMATION.
                     
                     If there is no material for a specific subject or topic, please indicate that the content is 
                     contained in the image portion of the file and cannot be summarized.
                     
                     Please do not provide any additional information beyond the summary. No follow-up questions or comments 
                     and no introductory remarks. Just the summary.
                  """

        display(Markdown("**Summarizing your material...**"))
        time.sleep(1)
        clear_output(wait=True)
        summary = ai.get_response(prompt)
        display(Markdown(summary))
        return summary

