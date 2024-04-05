import pandas as pd
import sys

labels = pd.read_csv('labels.csv')
dataframes = []

for index, row in labels.iterrows():
    npt_file = row['filename'].replace('.pcap', '.npt')
    npt_df = pd.read_csv(f'/path/to/the/npt/files/{npt_file}')
    npt_df['label'] = row['label']
    dataframes.append(npt_df)
    print(row['label'], file=sys.stdout)
    
    
dataset = pd.concat(dataframes, ignore_index=True)

dataset.to_csv('labeled_dataset.csv', index=False)
