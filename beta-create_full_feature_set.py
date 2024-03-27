import pandas as pd
import sys
import os

# Function to process npt files iteratively
def process_npt_files(pcap_directory, output_directory, labels_file):
    labels = pd.read_csv(labels_file)

    for index, row in labels.iterrows():
        npt_file = row['filename'].replace('.pcap', '.npt')
        npt_df = pd.read_csv(os.path.join(pcap_directory, npt_file))
        npt_df['label'] = row['label']
        yield npt_df

# Paths and directories
pcap_directory = "/path/to/the/npt/files"
labels_file = "labels.csv"
output_file = "labeled_dataset.csv"

# Create an iterator for processing npt files
dataframes_iter = process_npt_files(pcap_directory, labels_file)

# Process npt files iteratively and concatenate them
first_df = next(dataframes_iter)
dataset = pd.concat([first_df] + list(dataframes_iter), ignore_index=True)

# Save the concatenated DataFrame to a CSV file
dataset.to_csv(output_file, index=False)
