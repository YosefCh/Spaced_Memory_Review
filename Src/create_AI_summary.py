from query_runner import run_query
from AI_class import OpenAIClient
from IPython.display import display, Markdown, clear_output
import time

def generate_summary():
    user_input = display(Markdown("**Please enter which material you want to summarize.**"))
    run_query()