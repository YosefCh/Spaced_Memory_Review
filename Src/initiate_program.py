from datetime import datetime, timedelta
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
    """Ensure necessary folders exist."""
    print("\nChecking if the necessary file folders exist...\n")
    time.sleep(1.6)
    all_exist = True
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            all_exist = False
    if all_exist:
        print('The folders already exist.')
    else:
        print('The folders have been created successfully.')

def initiate_program():
    """Main function to initiate the program."""
    if is_testing:
        print("\nRunning in TESTING MODE. Changes will not affect real data.\n")

    print("\nChecking if the data file exists...\n")
    time.sleep(1.6)
    if not os.path.exists(data_file):
        create_data_file()
    else:
        print("The data file already exists.")
    time.sleep(1.6)
    create_folders()
    print("You're all set. Start learning!!!\n")

if __name__ == '__main__':
    initiate_program()
    #reset_data_file()