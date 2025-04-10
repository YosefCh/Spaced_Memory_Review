from datetime import datetime, timedelta
import json
import os
import time


with open('config.json', "r") as f:
    paths = json.load(f)
    data_file = paths['data_file']
    folders = [paths['single_files_path'],paths['review_files_path']]

def create_data_file():
    with open(data_file, 'w') as Csv_file:
            # Write the header
            Csv_file.write('Index,Date,FilePath,Subject,Topic\n')

            # Generate 10 years' worth of dates from today
            start_date = datetime.now()
            years = 10
            for i in range(years * 365):  # Approximate for 10 years
                short_date = (start_date + timedelta(days=i)).strftime("%#m/%#d/%Y") 
                Csv_file.write(f"{i+1},{short_date},,,\n")
                # Empty placeholders for FilePath, Subject, and Topic
    print('The data file has been created and or reset successfully')
    
    
def create_folders():
    print("\nChecking if the necessary file folders exist...\n")
    time.sleep(1)
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
    print("\nChecking if the data file exists...\n")
    time.sleep(1)
    file_exists = os.path.exists(data_file)
    if file_exists:
        with open(data_file, 'r') as Csv_file:
                #content = Csv_file.read()
                files = sum(1 for line in Csv_file if 'C:' in line)
                if files > 0:
                    warning = input('Warning: The file contains learned material information. Do you want to overwrite it? (y for yes anything else for no): ')
                    if warning.lower() != 'y':
                        print('The file has not been overwritten')
                        
                    else:
                        danger = input(f"Are you sure you want to delete {files} records of learned material? Enter 'yes' to proceed: ")
                        if danger.lower() == 'yes':
                            print('The file has been reset successfully.')
                            create_data_file()
    else:        
        create_data_file()
    create_folders()  
    print("You're all set. Start learning!!!\n")  
        
if __name__ == '__main__':
    initiate_program()