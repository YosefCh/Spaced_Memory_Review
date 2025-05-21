from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from IPython.display import Markdown, display, HTML
import json
import os
import time

# Load configuration that stores necessary paths, API keys, and other settings
with open('config.json', "r") as f:
    paths = json.load(f)

# load the paths to where we will store the data file and the folders
data_file = paths['data_file']
folders = [paths['single_files_path'], paths['review_files_path']]

# Set a flag for testing mode
# This flag can be used to switch between testing and production modes
is_testing = True  # Set to True for testing mode

# Use separate paths for testing mode
if is_testing:
    data_file = paths['TTdata_file']
    folders = [paths['TTsingle_files_path'], paths['TTreview_files_path']]

def create_data_file(reset=False):
    """
    Create the data file for the spaced memory review program.

    Parameters:
    - reset (bool): If True, creates a new data file even if one already exists (used for the reset functionality). Default is False, in case
      user accidentally runs the initiate_program function which calls this one.
      
    Returns:
    - str: A message indicating the result of the function. 
           It returns "Timed out" if the user fails to provide valid input within the allowed attempts, or "Success" if the data file is 
           created successfully. This return value is used by the reset function to determine whether to display a reset message or not.
           
    This function prompts the user to select a review schedule duration 
    (in years or months) and calculates the total number of days for the program. 
    It writes the initial setup to the data file.
    """
    
    # creation of file is only done if the file does not yet exist (program has not been set up yet) or if the user has requested a reset
    if not os.path.exists(data_file) or reset:
        # prompt user for the duration of the review schedule
        display(Markdown("### Select the duration of the review schedule:"))
        display(HTML("Enter <strong>1</strong> for choosing the duration in <strong>years</strong>, or <strong>2</strong> for choosing the duration in <strong>months</strong>."))
        
        # set max attempts for user input to avoid infinite loops
        max_attempts = 5
        # Initialize attempt counters to count the number of attempts made by the user
        unit_attempts = 0
        
        # Loop until a valid input is received or the maximum attempts are reached
        while True:
            # increment the attempt counter for each loop iteration
            unit_attempts += 1 
            if unit_attempts > max_attempts:
                  # if the user has exceeded the maximum attempts, return 'Timed out' (to be used by the reset function to know not to display a
                  # successful reset message)
                  return 'Timed out'
              
            # assign variable duration to the user metric choice
            duration = input("Enter your choice (1 or 2): ")
            print('You entered:', duration)
            
            # ensure that the input is a digit and the integer value is either 1 or 2 
            if duration.isdigit() and int(duration) in [1, 2]:
                # convert the input to an integer
                duration = int(duration) 
                # if the input is valid, break out of the loop 
                break
            # ensure that response appears before the next prompt by using flush=True which forces the output to be written immediately
            else:
                # if the input is invalid, prompt the user to enter a valid input
                # this will be repeated until a valid input is received or the maximum attempts are reached
                print("Invalid input. Please enter 1 or 2.", flush=True)
            
        
        # After a valid input is received, set the duration to the number of days based on the user's choice       
        num_yr_mnth_attempts = 0 
        # same logic as before, but now we are counting the number of attempts to get a valid input for the duration in years or months      
        while True:
            num_yr_mnth_attempts += 1 
            if num_yr_mnth_attempts > max_attempts:
                return 'Timed out'
            
            # for the year choice
            if duration == 1:
                years = input("Enter the number of years (whole number between 1 - 15): ")
                if years.isdigit() and 1 <= int(years) <= 15:
                    years = int(years)
                    
                    # Calculate the end date based on the number of years
                    end_date = datetime.now() + relativedelta(years=years)
                    # Calculate the exact number of days needed as lines in the csv data file
                    # The +1 is to include the current day in the schedule
                    duration = (end_date - datetime.now()).days + 1
                    # break out of the loop if the input is valid
                    break
                else:
                    print("Invalid input. Please enter a whole positive number between 1 - 15.", flush=True)
            elif duration == 2:
                months = input("Enter the number of months (whole number between 1 - 36): ")
                if months.isdigit() and 1 <= int(months) <= 36:
                    months = int(months)
                    end_date = datetime.now() + relativedelta(months=months)
                    duration = (end_date - datetime.now()).days + 1
                    break
                else:
                    print("Invalid input. Please enter a whole positive number between 1 - 36.", flush=True)
        
        # After a valid input is received, create the data file            
        with open(data_file, 'w') as Csv_file:
            # Write the header columns to the CSV file
            Csv_file.write('Index,Date,FilePath,Subject,Topic\n')

            # get the current date as the first value
            start_date = datetime.now()
            for i in range(duration): 
                # format the date as MM/DD/YYYY and write it to the CSV file 
                short_date = (start_date + timedelta(days=i)).strftime("%#m/%#d/%Y")
                # Empty placeholders for FilePath, Subject, and Topic 
                Csv_file.write(f"{i+1},{short_date},,,\n") 
            # If the file is created successfully, return a success message (used by the reset function to display a successful reset message)
            return 'Created new data file'

    

def reset_data_file():
    """
    Reset the existing data file for the spaced memory review program.

    This function checks if a data file exists and, if so, prompts the user to confirm
    before overwriting it. It warns the user if existing records will be lost and 
    ensures multiple confirmations before deleting data. If confirmed, it calls 
    create_data_file(reset=True) to recreate the file.
    
    """
    # checks if the data file exists (if not, there is no need to reset it)
    if os.path.exists(data_file):
        with open(data_file, 'r') as Csv_file:
            # check if the file contains any records of learned material which is done by looking for a C: (file path)
            # use a generator expression to count the number of lines that contain 'C:'
            files = sum(1 for line in Csv_file if 'C:' in line)
        
        # if the file contains records, prompt the user to confirm before overwriting it
        if files > 0:
            warning = input(f'Warning: The file contains {files} records of learned material. Do you want to overwrite it? (y for yes, anything else for no): ')
            if warning.lower() != 'y':
                display(Markdown('The __reveiw schedule__ has not been reset.'))
                # if the user does not want to overwrite the file, exit the function
                return
            danger = input("Are you sure you want to delete all records? Enter 'yes' to proceed: ")
            if danger.lower() != 'yes':
                display(Markdown('The __reveiw schedule__ has not been reset.'))
                return
    # if the user confirms, proceed to reset the data file by using the rest=True argument to oveiride the check in that function for the exitsing file
    call_create_func = create_data_file(reset=True)
    
    # check if user entry has timed out as a result of too many invalid inputs
    if call_create_func == 'Timed out':
        display(HTML('<em><strong style="color: red">Repeated Invalid Input.&nbsp;</strong></em>Exiting the program.'))   
    else:
        print('The __reveiw schedule__has been reset successfully.')
    

def create_folders():
    """Create the folders to house the single day and review files."""
    
    # check if the folders exist, and if not, create them
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        

def initiate_program():
    """
    Main function to initiate the program.
    
    This function sets up the program environment, including data files and folders, 
    and presents an introductory message to the user. If a setup already exists, it 
    notifies the user and does not repeat initialization.
    """
    
    # just for testing purposes will be removed later
    if is_testing:
        print("\nRunning in TESTING MODE. Changes will not affect real data.\n")
        
    # if either the data file or the folders do not exist, prompt the user to set up the program
    # this is only necessary if some of the files or folders were tampered with as when running for the first time
    # there is no need to check, as they certainly do not exist
    if not os.path.exists(data_file) or not os.path.exists(folders[0]) or not os.path.exists(folders[1]):
        display(HTML("<h1 style='color:blue;'>Welcome to the <strong>Spaced Memory Review</strong> Program!</h1>"))
        display(Markdown("### This program will allow you to retain __*all*__ of your learning!!."))
        
        # call the create_data_file function to create the data file
        a = create_data_file()
        # check if the user entry has timed out as a result of invalid inputs
        if a == 'Timed out':
            display(HTML('<em><strong style="color: red">Repeated Invalid Input.&nbsp;</strong></em>Exiting the program.'))
            return
        
        # call the create_folders function to create the folders
        create_folders()
        # use sleep to allow the user to read the message as opposed to having all the information appear at once
        time.sleep(1.6)
        display(Markdown("#### Setting up the program...\n"))
        time.sleep(3)
        display(Markdown("#### You're all set. Start learning and Retaining!!!"))
    else:
        display(HTML("""<h3><strong>The program is already set up.</strong></h3><p>There is no need to run this cell each time.</p>If you want to reset the data file, please run the cell in the <strong>Reset Program</strong> section (at the bottom of this page).
            """))
 
 
        
#if __name__ == '__main__':
  #reset_data_file()