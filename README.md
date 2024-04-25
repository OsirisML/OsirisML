# OS Fingerprinting

Data processing and machine learning application of Packet Capture (.pcap) data to passively identify operating systems.

# Installation on Debian Linux:

`chmod +x configure/configure.sh`

`sudo configure/configure.sh`

OsirisML is currently only available for installation on Debian Linux because it is recommended to run on a server with high `RAM` capacity. Through basic testing, a *.pcap* file of about `8` gb is reccomended to have at least `128` gb of `RAM`.

`Ubuntu 22.04.4` is reccomended.

See `configure/installation_instructions.txt` for more information on how to install dependencies.

# Usage

The *.pcap* file should be placed in `data/pcap/`.

Run `./preprocessing/process_pcap.sh <pcap_file.pcap>` to preprocess the *.pcap* file.

-> This generates a *.csv* file to `/data/csv/`.

Run `python3 xgboostmodel.py <csc_file.csv> <model_name> <OPTIONAL: test size (ex. 0.25, 0.2 by default)>`

-> This generates a *.json* model to `model/json/` and also outputs the model metrics like accuracy and F1 score.

**To test unseen data**:

There is a `friday_model.json` file in `model/json` that can be run with `python3 testmodel.py friday_model.json <data_to_test.csv>` or another *json* model.

Convert the unseen *.pcap* data to *.csv* with `preprocessing/nprint.sh` and `preprocessing/npt_to_csv.py`. This is the same preprocessing as `preprocessing/process_pcap.sh`, except it doesn't use `preprocessing/tcp_dump.sh`, since the actual OSes are unknown.

-> This is how you would actually use a model to **passively** identify operating systems on unseen data.

# Overview of Workflow

[Workflow Diagram PDF](OsirisML.pdf)

This open-source tool is built off the work on passive OS detection using nprint and nprintML.

https://arxiv.org/pdf/2008.02695.pdf

**Preprocessing - /preprocessing/process_pcap.sh**

1. Labeling each source IP to its OS

Given a *.pcap* file and identifying source IPs, `preprocessing/tcp_dump.sh` is run to call `tcpdump` on the *.pcap* file for each source IP, so the model is given classiciation labels for each element. `tcpdump` takes arguments of the source IP and corresponding OS. **The source IP's must be provided in**  `preprocessing/tcp_dump.sh`.

https://www.tcpdump.org/

2. Converting *.pcap* to tabular data *.npt*

Using nprint, the open-source *.pcap* preprocessing tool, the *.pcap* data is transformed into *.npt* data.

This runs in `preprocessing/nprint.sh`

https://github.com/nprint/nprint

Note: OSirisML is configured to work with `nprint-1.2.1`. To use a newer version, **see nprint's github for installation instructions** and replace the `tar` file in `configure`.

3. Combine the *.npt* files to a single labeled *csv* file.

These *.npt* files are combined to a single *csv* file using a custom `Python` script in `preprocessing`.

This script appends the corresponding label identified from the source IP to the last column of the *csv* file.

**Machine Learning Application**

4. Apply machine learning model, XGBoost, to the labeled tabular data to create a classification model.

This *csv* file is split into `X_train`, `X_test`, `Y_train`, and `Y_test` data, where X is the `960` attributes of tabular data, and Y is the corresponding operating system classification. This is done with `Pandas`, an open-source data manipulation tool, and `scikit-learn`, an open-source machine learning Python library.

https://pandas.pydata.org/

https://scikit-learn.org/stable/

The payload and source IP bytes of the packet are dropped from the dataframe and not considered in the model to avoid data leakage and overfitting.

This data is trained using `XGBoost`, an open-source machine learning tool that uses gradient boosting. By default, a test size of `0.2` is used, unless specified as an additional sys argument. See usage for `model/xgboostmodel.py`.

https://xgboost.readthedocs.io/en/stable/


**Additional Steps**

5. Mine for optimal parameters specific to the .csv file with `param_finder_xgboost_from_csv.py`. Note there is an alternative param miner script that takes 4 .npy files as input instead of a single .csv.

-> Modify the param_grid to specify the parameters to mine for. See `https://xgboost.readthedocs.io/en/stable/parameter.html` for all parameters.

6. Retrain model on additional CSV data with `model/trainmodel.py`. Run `python3 model/trainmodel.py` for usage.

7. Test a model on unseen CSV data. Run `python3 model/testmodel.py` for usage.

# Results with CIC-IDS2017 Dataset

Using *Friday-WorkingHours.pcap* from

`http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/CIC-IDS-2017/PCAPs/`, which is a 8.2 gb *.pcap* file with over 4.5 million samples,

saw an Accuracy score of **84.91%** with an F1 Score of **82.96%**.

Data split: 80% Training/validation, 20% testing.

This was run on a VM operating `Ubuntu 22.04.4` with 128 gb of RAM.

# Default OSes and Source IP's in preprocessing/tcp_dump.sh

Here is the table provided by University of New Brunswick, which is are the default OSes in `preprocessing/tcp_dump.sh`:
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

To generate a new model with different OSes (and source IP's), modify the `preprocessing/tcp_dump.sh` script.

# Implementation with New PCAP Data

To use OSirisML with any dataset, the network data needs to be sorted by source IP. This is done best in a controlled environment, where each source IP is a unique OS.

Modify the `preprocessing/tcp_dump.sh` script to label each source IP with the corresponding operating system.

# Testing Data

To test model creation:

There is a `zip` file in `data/csv/` that you can `unzip` to retrieve a .csv file to test creating models with.

To test the preprocessing:

There is a `tar.gz` file in `data/pcap/` that has 13 different pcap files for each OS and already had `preprocessing/tcp_dump.sh` run. Extract the tar file with `tar -xzf friday_32_pcaps.tar.gz` (while in the `data/pcap/` directory), and the files will be put into `data/pcap/pcap_os_split/`, where the scripts in `preprocessing` are expecting them to be.
