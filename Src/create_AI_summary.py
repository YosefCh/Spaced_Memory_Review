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
        

    def find_files(self, quiz=False):
        if quiz:
            display(Markdown("**Please enter which material you want to generate a quiz for:**"))
        else:
            display(Markdown("**Please enter which material you want to summarize:**"))
        question = input("Your question: ")
        time.sleep(1)
        natural_language_to_query(question, display_output=False, purpose="summary")
        
        df = pd.read_csv(self.query_output_file)
        files = df['FilePath'].dropna().tolist()
        subjects = df['Subject'].dropna().tolist()
        topics = df['Topic'].dropna().tolist()
        return files, subjects, topics

    def extract_material(self, quiz=False):
     try:
        files, subjects, topics = self.find_files(quiz=quiz)
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
     except Exception as e:
        display(Markdown(f"**An error occurred while extracting material:\n{e}**"))
        return "Error extracting material."

    
    def generate_summary(self):
        material_content = self.extract_material()
        if material_content.strip() == "Error extracting material.":
            return None
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
    
    def generate_quiz(self, difficulty="medium", interactive=False):
     try:
        content = self.extract_material(quiz=True)
        # MUST ADD A CHECK TO SEE IF CONTENT IS EMPTY
        if not content.strip():
            display(Markdown("**No content available for quiz generation.**"))
            return None

        ai = OpenAIClient(system_role_content="You are an expert at creating quizzes based on educational material.")
        prompt = f"""Based on the following content, create a quiz of {difficulty} difficulty level.
                     Here is the content:\n\n{content}\n\n:
                     Each question should have 4 multiple-choice answers, with one correct answer.
                     Please format the quiz as follows:
                     
                     Question 1: [Question text (bolded)]
                     
                     A. [Option A]
                     B. [Option B]
                     C. [Option C]
                     D. [Option D]
                     
                     Question 2: [Question text (bolded)]
                     
                     A. [Option A]
                     B. [Option B]
                     C. [Option C]
                     D. [Option D]
                        ...
                     Correct Answers: [Correct option letter for each question in order]
                     
                     Repeat this format for all questions.
                    
                    IMPORTANT: THE QUESTIONS AND ANSWERS SHOULD BE BASED ON THE EXACT CONTENT PROVIDED, EVEN IF IT IS NOT NECESSARILY THE TYPICAL WAY OF PRESENTING 
                    Additionally, please do not provide any additional information beyond the quiz. No follow-up questions or comments 
                    and no introductory remarks. Just the quiz.
                  """

        display(Markdown("**Generating quiz...**"))
        time.sleep(1)
        clear_output(wait=True)
        quiz = ai.get_response(prompt)
        display(Markdown(quiz))
        return quiz
     except Exception as e:
        display(Markdown(f"**An error occurred while generating the quiz:\n{e}**"))
        return None

