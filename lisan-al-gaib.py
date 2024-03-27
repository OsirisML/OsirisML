import pandas as pd
import os
import sys

def process_and_write_npt_files(pcap_directory, output_directory, labels_file, output_file):
    labels = pd.read_csv(labels_file)
    
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Open output CSV file in append mode
    with open(os.path.join(output_directory, output_file), 'a') as f_output:
        is_header_written = False
        
        for index, row in labels.iterrows():
            npt_file = row['filename'].replace('.pcap', '.npt')
            npt_file_path = os.path.join(pcap_directory, npt_file)
            print(npt_file_path, file=sys.stdout)
            if os.path.exists(npt_file_path):
                npt_df = pd.read_csv(npt_file_path)
                npt_df['label'] = row['label']
                
                # Write DataFrame to CSV file, control header writing to avoid repetition
                npt_df.to_csv(f_output, header=not is_header_written, index=False)
                print(row['label'], file=sys.stdout)
                if not is_header_written:
                    is_header_written = True

# Paths and directories
pcap_directory = os.path.expanduser("~/Documents/SecureCapstone/os_detection_data/thursday-npt")
output_directory = os.path.expanduser("~/Documents/SecureCapstone/os_detection_data")
labels_file = "labels.csv"
output_file = "labeled_dataset.csv"

# Call the function
process_and_write_npt_files(pcap_directory, output_directory, labels_file, output_file)
