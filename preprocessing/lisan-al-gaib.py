import pandas as pd
import os
import sys

# "npt_to_csv.py"
# This file takes the split npt files by OS and combines them into one CSV file
# Note: This file assumes the npt files are located in ../data/npt/npt_os_split
#   The csv file will be written to ../data/csv

def process_and_write_npt_files(npt_directory, output_csv_directory, output_file):
    labels = pd.read_csv(os.path.abspath(os.path.join("..", "labels", "labels.csv")))
    
    # Ensure output directory exists
    if not os.path.exists(output_csv_directory):
        os.makedirs(output_csv_directory)
    
    # Open output CSV file in append mode
    with open(os.path.join(output_csv_directory, output_file), 'a') as f_output:
        is_header_written = False
        
        for index, row in labels.iterrows():
            npt_file = row['filename'].replace('.pcap', '.npt')
            npt_file_path = os.path.join(npt_directory, npt_file)
            print(npt_file_path, file=sys.stdout)
            if os.path.exists(npt_file_path):
                npt_df = pd.read_csv(npt_file_path)
                npt_df['label'] = row['label']
                
                # Write DataFrame to CSV file, control header writing to avoid repetition
                npt_df.to_csv(f_output, header=not is_header_written, index=False)
                print(row['label'], file=sys.stdout)
                if not is_header_written:
                    is_header_written = True
    print("Created csv file " + output_file + "in directory " + output_csv_directory + "\n")


# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 [this_script].py output_filename.csv")
    sys.exit(1)  # Exit with error code 1

npt_directory = "../data/npt/npt_os_split"
output_csv_directory = "../data/csv"
output_file = sys.argv[1]

# Call the function
process_and_write_npt_files(npt_directory, output_csv_directory, output_file)