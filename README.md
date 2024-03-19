# OS_MLFingerprinting

Use modern machine learning algorithms to improve upon the Passive OS fingerprinting completed in https://arxiv.org/pdf/2008.02695.pdf

Replicating section 5.2 with xgboost saw an Accuracy score of 74.38% with an F1 Score of 75.48%

To create the appropriate labels use tcpdump to separate the source IP addresses into 13 separate pcap files, then run the label generation script provided in the paper above.

Here is the table provided by University of New Brunswick:
Web server 16 Public: 192.168.10.50, 205.174.165.68
Ubuntu server 12 Public: 192.168.10.51, 205.174.165.66
Ubuntu 14.4, 32B: 192.168.10.19
Ubuntu 14.4, 64B: 192.168.10.17
Ubuntu 16.4, 32B: 192.168.10.16
Ubuntu 16.4, 64B: 192.168.10.12
Win 7 Pro, 64B: 192.168.10.9
Win 8.1, 64B: 192.168.10.5
Win Vista, 64B: 192.168.10.8
Win 10, pro 32B: 192.168.10.14
Win 10, 64B: 192.168.10.15
MAC: 192.168.10.25
Kali: 205.174.165.73

Use the pcap_to_nprint script to convert all the pcaps into npt format.
Use the create_full_feature_set script to add the appropriate labels to the dataset.

Once the full feature dataset has been acquired, it can now be split by sklearn and used with ML algorithms
