import pandas as pd
import os
import sys

# "npt_to_csv.py"
# This file takes the split npt files by OS and combines them into one CSV file
# Note: This file assumes the npt files are located in ../data/npt
#   The csv file will be written to ../data/csv

def process_and_write_npt_files(npt_directory, output_csv_directory, output_file):
    labels = pd.read_csv(os.path.abspath(os.path.join("..", "labels", "labels.csv")))
    
    # Ensure output directory exists
    if not os.path.exists(output_csv_directory):
        os.makedirs(output_csv_directory)
        print("Created new output dir: " + output_csv_directory)
    
    # Open output CSV file in write mode
    with open(os.path.join(output_csv_directory, output_file), 'w') as f_output:
        is_header_written = False
        
        for npt_filename in os.listdir(npt_directory):
            print("Processing all .npt files in " + npt_directory)
            if npt_filename.endswith('.npt'):
                npt_file_path = os.path.join(npt_directory, npt_filename)
                try:
                    print("Writing file " + npt_filename + " to csv...")
                    npt_df = pd.read_csv(npt_file_path)
                    
                    # Extract label from filename (remove extension)
                    label = os.path.splitext(npt_filename)[0]
                    npt_df['label'] = label
                    
                    # Write DataFrame to CSV file, control header writing to avoid repetition
                    npt_df.to_csv(f_output, header=not is_header_written, index=False, mode='a' if is_header_written else 'w')
                    print("Finished writing file " + npt_filename + " to csv.")
                    if not is_header_written:
                        is_header_written = True
                except Exception as e:
                    print("ERROR:", e)
                    print("Error processing file " + npt_filename + " in " + npt_directory)

    print("Created csv file " + output_file + " in directory " + output_csv_directory + "\n")


npt_directory = "../data/npt"

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 <this_script.py> <output_filename.csv>")
    print("All .npt files must be in " + npt_directory)
    sys.exit(1)  # Exit with error code 1


output_csv_directory = "../data/csv"
output_file = sys.argv[1]

# Call the function
process_and_write_npt_files(npt_directory, output_csv_directory, output_file)
