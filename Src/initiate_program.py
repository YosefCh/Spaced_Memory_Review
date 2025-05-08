from datetime import datetime, timedelta
from IPython.display import Markdown, display, HTML
import json
import os
import time

# Load configuration
with open('config.json', "r") as f:
    paths = json.load(f)

data_file = paths['data_file']
folders = [paths['single_files_path'], paths['review_files_path']]
is_testing = True  # Set to True for testing mode

# Use separate paths for testing mode
if is_testing:
    data_file = paths['TTdata_file']
    folders = [paths['TTsingle_files_path'], paths['TTreview_files_path']]

def create_data_file():
    """Create a new data file."""
    # we must check if the file exists as the initiate_program funcion will call this function as
    # long as either the data file or the folders do not exist. If we do not check for the file, it will be OVERWRITTEN LOSING ALL THE DATA
    if not os.path.exists(data_file):
        with open(data_file, 'w') as Csv_file:
            # Write the header
            Csv_file.write('Index,Date,FilePath,Subject,Topic\n')

            # Generate 10 years' worth of dates from today
            start_date = datetime.now()
            years = 10
            for i in range(years * 365):  # Approximate for 10 years
                short_date = (start_date + timedelta(days=i)).strftime("%#m/%#d/%Y") 
                Csv_file.write(f"{i+1},{short_date},,,\n")  # Empty placeholders for FilePath, Subject, and Topic

    

def reset_data_file():
    """Reset the existing data file."""
    if os.path.exists(data_file):
        with open(data_file, 'r') as Csv_file:
            files = sum(1 for line in Csv_file if 'C:' in line)
        
        if files > 0:
            warning = input(f'Warning: The file contains {files} records of learned material. Do you want to overwrite it? (y for yes, anything else for no): ')
            if warning.lower() != 'y':
                print('The file has not been overwritten.')
                return
            danger = input("Are you sure you want to delete all records? Enter 'yes' to proceed: ")
            if danger.lower() != 'yes':
                print('The file has not been reset.')
                return
    
    create_data_file()
    print('The data file has been reset successfully.')
    

def create_folders():
    """Create the folders to house the single day and review files."""
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        

def initiate_program():
    """Main function to initiate the program."""
    if is_testing:
        print("\nRunning in TESTING MODE. Changes will not affect real data.\n")
    if not os.path.exists(data_file) or not os.path.exists(folders[0]) or not os.path.exists(folders[1]):
        display(HTML("<h1 style='color:blue;'>Welcome to the <strong>Spaced Memory Review</strong> Program!</h1>"))
        display(Markdown("### This program will allow you to retain __*all*__ of your learning!!."))
        create_data_file()
        create_folders()
        time.sleep(1.6)
        display(Markdown("#### Setting up the program...\n"))
        time.sleep(3)
        display(Markdown("#### You're all set. Start learning and Retaining!!!"))
    else:
        print("""The program is already set up.\nThere is no need to run this cell each time.\nIf you want to reset the data file, please run the reset_data_file cell at the bottom of this page.
            """)
 
 
        
if __name__ == '__main__':
    initiate_program()
    #reset_data_file()