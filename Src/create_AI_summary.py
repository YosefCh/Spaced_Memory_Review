from AI_text_to_query_converter import natural_language_to_query
from AI_class import OpenAIClient, Reasoning_OpenAIClient
from IPython.display import display, Markdown, clear_output
import time
import pandas as pd
import os
import math

class AISummaryTool:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.query_output_file = os.path.join(self.BASE_DIR, "query_output.csv")
        

    def find_files(self, quiz=False):
     try:
        if quiz:
            display(Markdown("**Please enter which material you want to generate a quiz for:**"))
        else:
            display(Markdown("**Please enter which material you want to summarize:**"))
        question = input("Submit Material here: ")
        # display(Markdown(f"Your Entered: __{question}__"))
        time.sleep(1)
        natural_language_to_query(question, display_output=False, purpose="summary")
        
        df = pd.read_csv(self.query_output_file)
        files = df['FilePath'].dropna().tolist()
        subjects = df['Subject'].dropna().tolist()
        topics = df['Topic'].dropna().tolist()
        # get length of files to use later to tell program how many questions to generate
        self.num_files = len(files)
        return files, subjects, topics
     except Exception as e:
         display(Markdown(f"**An error occurred while finding files:\n{e}**"))
         return [], [], []

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

                # extra check to ensure that the base 64 images are removed
                base64_pos = section_content.find('png;base64')
                if base64_pos != -1:  # Only truncate if "base64" is found
                   section_content = section_content[:base64_pos]
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
        
        # Initialize the AI client to gpt 5.1 and  with high reasoning and verbosity for better summaries
        ai = Reasoning_OpenAIClient(model_name="gpt-5.1", reasoning="high", verbosity="high", system_role_content="You are an expert at summarizing educational material.")
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
        
        # if token limit is reached fallback to standard OpenAIClient
        if summary.startswith("An error occurred"):
            backup_ai = OpenAIClient(model_name="gpt-4.1-mini", system_role_content="You are an expert at summarizing educational material.")
            summary = backup_ai.get_response(prompt)
        display(Markdown(summary))
        return summary
        

    def generate_quiz(self, difficulty="intermediate", interactive=False):
     try:
        content = self.extract_material(quiz=True)
        # MUST ADD A CHECK TO SEE IF CONTENT IS EMPTY
        if not content.strip():
            display(Markdown("**No content available for quiz generation.**"))
            return None
        
        if difficulty == "advanced":
            quiz_length = self.num_files * 2  # e.g., 2 questions per file
        elif difficulty == "intermediate":
            quiz_length = math.ceil(self.num_files * 1.5)  # approximately 1.5 questions per file
        elif difficulty == "beginner":
            quiz_length = self.num_files * 1  

        # Display quiz generation message
        # The difficulty parameter is passed from the quiz_level method in the summary notebook
        display(Markdown(f"**Generating {difficulty} level quiz with {quiz_length} questions...**"))
        
        if not interactive:
            ai = Reasoning_OpenAIClient(model_name="gpt-5.1", reasoning="high", verbosity="high", system_role_content="You are an expert at creating quizzes based on educational material.")
            prompt = f"""Based on the following content, create a quiz of {difficulty} level difficulty.
                        Here is the content:\n\n{content}\n\n
                        
                        QUIZ LENGTH:
                        The quiz should contain exactly {quiz_length} questions.
                        
                        Each question should have 4 multiple-choice answers, with one correct answer.
                        Please format the quiz exactly as follows:
                        
                        **Question 1: [Question text]**
                        
                        A. [Option A]
                        B. [Option B]
                        C. [Option C]
                        D. [Option D]
                        
                        
                        **Question 2: [Question text]**
                        
                        A. [Option A]
                        B. [Option B]
                        C. [Option C]
                        D. [Option D]
                        
                        
                        
                        **Question 3: [Question text]**
                        
                        A. [Option A]
                        B. [Option B]
                        C. [Option C]
                        D. [Option D]
                        
                        ...
                        
                        **Correct Answers:** [List answers like: 1-A, 2-B, etc.]
                        
                        IMPORTANT: THE QUESTIONS AND ANSWERS SHOULD BE BASED ON THE EXACT CONTENT PROVIDED.
                        Do not provide any additional information beyond the quiz. No follow-up questions, comments, or introductory remarks. Just the quiz in the exact format shown above.
                    """

            time.sleep(1.8)
            clear_output(wait=True)
            quiz = ai.get_response(prompt)
            
            # if token limit is reached fallback to standard OpenAIClient
            if quiz.startswith("An error occurred"):
                backup_ai = OpenAIClient(model_name="gpt-4.1-mini", system_role_content="You are an expert at creating quizzes based on educational material.")
                quiz = backup_ai.get_response(prompt)
            display(Markdown(quiz))
            return quiz
        else:
            ai = Reasoning_OpenAIClient(model_name="gpt-5.1", reasoning="high", verbosity="high", system_role_content="You are an expert at creating quizzes based on educational material.")
            
            if difficulty == "advanced":
                quiz_length = self.num_files * 2  # e.g., 2 questions per file
            elif difficulty == "intermediate":
                quiz_length = math.ceil(self.num_files * 1.5)  # approximately 1.5 questions per file
            elif difficulty == "beginner":
               quiz_length = self.num_files * 1  
            
            prompt = f"""Based on the following content, create a quiz of {difficulty} difficulty level.
                        Here is the content:\n\n{content}\n\n
                        
                        QUIZ LENGTH:
                        The quiz should contain exactly {quiz_length} questions.
                        
                        Return the response as a single string that I can split using triple pipes (|||) as a separator.

                        CRITICAL FORMATTING REQUIREMENTS:
                        - Use TRIPLE PIPES (|||) after EVERY element EXCEPT the very last one
                        - First {quiz_length} elements: formatted questions with options
                        - Last {quiz_length} elements: correct answers (just the letter: A, B, C, or D)

                        The exact format should be:
                        **Question 1: [Question text]**

                        A. [Option A]
                        B. [Option B]
                        C. [Option C]
                        D. [Option D]|||


                        **Question 2: [Question text]**

                        A. [Option A]
                        B. [Option B]
                        C. [Option C]
                        D. [Option D]|||


                        **Question 3: [Question text]**

                        A. [Option A]
                        B. [Option B]
                        C. [Option C]
                        D. [Option D]|||A|||B|||C

                        etc..

                        Return ONLY the formatted string above with triple pipes as separators. NO extra text, explanations, or formatting.
                        
                        IMPORTANT: THE QUESTIONS AND ANSWERS SHOULD BE BASED ON THE EXACT CONTENT PROVIDED.
                        Return only the single list above, nothing else.
                    """

            time.sleep(1.8)
            clear_output(wait=True)
            quiz = ai.get_response(prompt)
            
            # if token limit is reached fallback to standard OpenAIClient
            if quiz.startswith("An error occurred"):
                backup_ai = OpenAIClient(model_name="gpt-4.1-mini", system_role_content="You are an expert at creating quizzes based on educational material.")
                quiz = backup_ai.get_response(prompt)
            
            data = quiz.split('|||')
            questions = data[:len(data)//2]
            answers = data[len(data)//2:]
            score = 0
            wrong_answers = []
            for i in range(len(questions)):
                display(Markdown(questions[i]))
                user_answer = input("Your answer (A, B, C, or D): ").strip().upper()
                correct_answer = answers[i].strip().upper()
                clear_output(wait=True)
                if user_answer == correct_answer:
                    score += 1
                else:
                    wrong_answers.append((questions[i], correct_answer))
            display(Markdown(f" # **Your Score: {score / len(questions) * 100:.0f}%**"))
            if score / len(questions) * 100 < 100:
                display(Markdown("---"))  # Horizontal line separator
                display(Markdown(" ## **Please review the correct answers for the questions you answered incorrectly:**"))
                for error in wrong_answers:
                    display(Markdown(f"{error[0]}\n\n**Correct Answer: {error[1]}**"))

     except Exception as e:
        display(Markdown(f"**An error occurred while generating the quiz:\n{e}**"))
        return None


    def quiz_level(self):
        """
        This method is called in the summary notebook to feed the difficulty level into the quiz generation function.
        """
        display(Markdown("__Choose the number corresponding the level of difficulty for your quiz__"))
        display(Markdown("1.  beginner"))
        display(Markdown("2.  intermediate"))
        display(Markdown("3.  advanced"))
        choice = input("Select quiz difficulty (beginner, intermediate, advanced): ")
        attempts = 0
        while True: 
            if choice in ['1', '2', '3']:
                level_map = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
                level = level_map[choice]
                # display(Markdown(f"**You have selected '{level}' difficulty for your quiz.**"))
                time.sleep(1)
                break
            else:
                choice = input("Invalid choice. Please select a number from 1 to 3: ")
            attempts += 1
            if attempts >= 3:
                print("Too many invalid attempts. Defaulting to 'medium' difficulty.")
                level = "medium"
                break
        return level