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

def create_data_file(reset=False):
    # reset: bool = False
    # this is needed to be able to have the function called in the reset_data_file function where we will set reset=True
    # and overide checking if the data file exists since we want to create a new one despite it already existing.
    """Create a new data file."""
    # we must check if the file exists as the initiate_program funcion will call this function as
    # long as either the data file or the folders do not exist. If we do not check for the file, it will be OVERWRITTEN LOSING ALL THE DATA
    if reset or not os.path.exists(data_file):
        # prompt user for the duration of the review schedule
        display(Markdown("### Select the duration of the review schedule:"))
        display(HTML("Enter <strong>1</strong> for choosing the duration in <strong>years</strong>, or <strong>2</strong> for choosing the duration in <strong>months</strong>."))
        
        max_attempts = 5
        attempts = 0
        
        while True:
            attempts += 1 
            if attempts > max_attempts:
                  print("Maximum attempts reached. Exiting the program.")
                  return 'Timed out'
            duration = input("Enter your choice (1 or 2): ")
            print('You entered:', duration)
                
            if duration.isdigit() and int(duration) in [1, 2]:
                duration = int(duration)  
                break
            # ensure that response appears before the next prompt by using flush=True which forces the output to be written immediately
            else:
                print("Invalid input. Please enter 1 or 2.", flush=True)
            
               
                
        for i in range(max_attempts): 
            if duration == 1:
                years = input("Enter the number of years (whole number between 1 - 15): ")
                if years.isdigit() and 1 <= int(years) <= 15:
                    years = int(years)
                    # Approximate the number of days in a year as 365
                    duration = years * 365
                    break
                else:
                    print("Invalid input. Please enter a whole positive number between 1 - 15.", flush=True)
            elif duration == 2:
                months = input("Enter the number of months (whole number between 1 - 36): ")
                if months.isdigit() and 1 <= int(months) <= 36:
                    months = int(months)
                    # Approximate the number of days in a month as 30
                    duration = months * 30
                    break
                else:
                    print("Invalid input. Please enter a whole positive number between 1 - 36.", flush=True)
        with open(data_file, 'w') as Csv_file:
            # Write the header
            Csv_file.write('Index,Date,FilePath,Subject,Topic\n')

            # Generate 10 years' worth of dates from today
            start_date = datetime.now()
            for i in range(duration):  # Approximate for 10 years
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
                display(Markdown('The __reveiw schedule__ has not been reset.'))
                return
            danger = input("Are you sure you want to delete all records? Enter 'yes' to proceed: ")
            if danger.lower() != 'yes':
                display(Markdown('The __reveiw schedule__ has not been reset.'))
                return
    
    create_data_file(reset=True)
    display(Markdown('The __reveiw schedule__ has been reset successfully.'))
    

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
        display(HTML("""<h3><strong>The program is already set up.</strong></h3><p>There is no need to run this cell each time.</p>If you want to reset the data file, please run the cell in the <strong>Reset Program</strong> section (at the bottom of this page).
            """))
 
 
        
if __name__ == '__main__':
  reset_data_file()