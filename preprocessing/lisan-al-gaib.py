import pandas as pd
import os
import sys

def process_and_write_npt_files(npt_directory, output_file):
    labels = pd.read_csv(os.path.abspath(os.path.join("..", "labels", "labels.csv")))
    
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Open output CSV file in append mode
    with open(os.path.join(npt_directory, output_file), 'a') as f_output:
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


# Check if the correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 our_script.py path_to_npt_directory output_filename.csv\nWARNING: If you name the output file the same as one of the input files, the output file will overwrite the input file.")
    sys.exit(1)  # Exit with error code 1

# Extract the npt directory path and output file name from the command line arguments
npt_directory = sys.argv[1]
output_file = sys.argv[2]

# Call the function
process_and_write_npt_files(npt_directory, output_file)