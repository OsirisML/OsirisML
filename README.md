# OS Fingerprinting

Data processing and machine learning application of Packet Capture (.pcap) data to passively identify operating systems.

# Installation on Debian Linux:

`git clone https://github.com/osirisml/osirisml.git`

`chmod +x configure/configure.sh`

`sudo configure/configure.sh`

OsirisML is currently only available for installation on Debian Linux because it is recommended to run on a server with high RAM capacity. Through basic testing, a *.pcap* file of about 8 gb is reccomended to have at least 128 gb of RAM.

*Ubuntu 22.04.4* is reccomended.

See *configure/installation_instructions.txt* for more information on how to install dependencies.

# Overview and Basic Usage

There are two phases to OsirisML - preprocessing and ML application.

[Workflow Diagram JPEG](OsirisML.jpeg)

To preprocess the data, run:

`./preprocessing/process_pcap.sh <pcap_file.pcap>`

To generate a model with the resulting *csv*, run:

`python3 xgboostmodel.py <csv_file.csv> <model_name.json>`

-> This generates a *json* model to *model/json/* and also outputs the model metrics like accuracy and F1 score.

**To test unseen data**:

There is a *friday_model.json* file in *model/json* that can be run with:

`python3 testmodel.py friday_model.json <data_to_test.csv>` or another *json* model.

See Phase 2 for more usage.

# Preprocessing

In the *preprocessing/* directory, this entire phase can simply be run with:

`./process_pcap.sh <pcap_file.pcap>`

which calls the following 3 scripts in succession to generate a *csv* to *data/csv/*:

1. **tcp_dump.sh** - Labels each source IP to its OS.

Usage: `./tcp_dump.sh`

Given a *.pcap* file and identifying source IPs, this script is run to call *tcpdump*` on the *.pcap* file for each source IP, so the model is given classiciation labels for each element. *tcpdump* takes arguments of the source IP and corresponding OS. **The source IP's must be provided in preprocessing/tcp_dump.sh**.

https://www.tcpdump.org/

2. **./nprint.sh** - Uses the open-source tool nPrint on all the *pcap* files.

Usage: `./nprint.sh`

This converts all *.pcap* files in *data/pcap/pcap_os_split/* to tabular *npt* files to *data/npt/*.

https://github.com/nprint/nprint

Note: OSirisML is configured to work with *nprint-1.2.1*. To use a newer version, **see nprint's github for installation instructions** and replace the *tar* file in *configure/*.

3. **npt_to_csv.py** - combines all the *.npt* files to a single labeled *csv* file placed into *data/csv/*.

Usage: `npt_to_csv.py <new_file.csv>`

This script appends the corresponding label identified from the source IP to the last column of the *csv* file.

# Machine Learning Application

Apply Machine Learning scripts in the *model* directory. All resulting *json* models will be in *model/json/*.

1. **xgboostmodel.py** - applies XGBoost, a machine learning tool, to the labeled tabular data to create a classification model.

Usage: `python3 xgboostmodel.py <data.csv> <modelname> <OPTIONAL: <decimal for test split size>`

By default, a test size of 0.2 is used.

2. **hyperparameter_tuning.py* - mines for optimal parameters specific to the *csv* file.

Usage: `python3 hyperparameter\_tuning.py <data.csv>`

-> Modify the param_grid to specify the parameters to mine for. Note that complex grids require immense time and resources.

See https://xgboost.readthedocs.io/en/stable/parameter.html for all parameters.

3. **trainmodel.py** - retrains a model on additional *csv* data.

Usage: `python3 trainmodel.py <current\_model.json> <data.csv> <new.json>`

4. **testmodel.py** - uses a supplied model to test a *csv* file. This is the **passive OS Fingerprinting** portion.

Usage: `python3 testmodel.py <model.json> <data.csv>`

https://xgboost.readthedocs.io/en/stable/

https://pandas.pydata.org/

https://scikit-learn.org/stable/

# Results with CIC-IDS2017 Dataset

Using *Friday-WorkingHours.pcap* from

http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/CIC-IDS-2017/PCAPs/

which is a 8.2 gb *.pcap* file with over 4.5 million samples,

saw an Accuracy score of **84.91%** with an F1 Score of **82.96%**.

Data split: 80% Training/validation, 20% testing.

This was run on a VM operating *Ubuntu 22.04.4* with 128 gb of RAM.

# Default OSes and Source IP's in preprocessing/tcp_dump.sh

Here is the table provided by University of New Brunswick, which is are the default OSes in *preprocessing/tcp_dump.sh*:
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

To generate a new model with different OSes (and source IP's), modify the *preprocessing/tcp_dump.sh* script.

# Implementation with New PCAP Data

To use OSirisML with any dataset, the network data needs to be sorted by source IP. This is done best in a controlled environment, where each source IP is a unique OS.

Modify the *preprocessing/tcp_dump.sh* script to label each source IP with the corresponding operating system.

# Testing Data

To test model creation:

There is a *zip* file in *data/csv/* that you can unzip to retrieve a .csv file to test creating models with.

To test the preprocessing:

There is a *tar.gz* file in *data/pcap/* that has 13 different pcap files for each OS and already had *preprocessing/tcp_dump.sh* run. Extract the tar file with `tar -xzf friday_32_pcaps.tar.gz` (while in the *data/pcap/* directory), and the files will be put into *data/pcap/pcap_os_split/*, where the scripts in *preprocessing* are expecting them to be.
