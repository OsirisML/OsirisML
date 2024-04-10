# OS_MLFingerprinting

Use modern machine learning algorithms to improve upon the Passive OS fingerprinting completed in https://arxiv.org/pdf/2008.02695.pdf

Replicating section 5.2 with xgboost saw an Accuracy score of 74.38% with an F1 Score of 75.48%

To create the appropriate labels use tcpdump to separate the source IP addresses into 13 separate pcap files, then run the label generation script provided in the paper above.

Here is the table provided by University of New Brunswick:
- Web server 16 Public: 192.168.10.50, 205.174.165.68
- Ubuntu server 12 Public: 192.168.10.51, 205.174.165.66
- Ubuntu 14.4, 32B: 192.168.10.19
- Ubuntu 14.4, 64B: 192.168.10.17
- Ubuntu 16.4, 32B: 192.168.10.16
- Ubuntu 16.4, 64B: 192.168.10.12
- Win 7 Pro, 64B: 192.168.10.9
- Win 8.1, 64B: 192.168.10.5
- Win Vista, 64B: 192.168.10.8
- Win 10, pro 32B: 192.168.10.14
- Win 10, 64B: 192.168.10.15
- MAC: 192.168.10.25
- Kali: 205.174.165.73

Use the pcap_to_nprint script to convert all the pcaps into npt format.
Use the create_full_feature_set script to add the appropriate labels to the dataset.

Once the full feature dataset has been acquired, it can now be split by sklearn and used with ML algorithms


TODO:

Ordered by priority tier.

Optimizing model:

- Optimize model with max_depth and eta params
- Retrain model on other datasets

Creating command line tool for generic use:

- Create single script to execute entire workflow
- Create small pcap file and test classes to test the scripts
- Have single command to execute workflow with params for: csv file for number and type of OSes, decimal value of training set size (pass in to xgboost.py, left to 0.2 by default if none given),
    option to remove data files after each step of workflow (remove the .pcaps after they are all converted to npt, then removed the .npts after they are all csv)
- Create test directory with small test pcap file (see nprint's repo)

Extra:

- Create markdown README with documentation and command line prints for errors and usage