# OsirisML - Passive OS Fingerprinting

Data processing and machine learning application of Packet Capture (.pcap) data to passively identify operating systems.

[Workflow Diagram](OsirisML.jpeg)

# Installation

OsirisML is currently only available for Debian Linux. It is recommended to run on a server with high RAM capacity. Through basic testing, a .pcap file of about 8 GB requires at least 128 GB of RAM. *Ubuntu 22.04.4* is recommended.

```
git clone https://github.com/osirisml/osirisml.git
cd osirisml
```

### Option 1: Using Make (recommended)

```
make install
```

### Option 2: Manual setup

Install nprint:

```
sudo apt-get install -y libpcap-dev g++ make
cd configure
tar -xvf nprint-1.2.1.tar.gz
cd nprint-1.2.1
./configure
make
sudo make install
cd ../..
```

Install Python dependencies:

```
pip install -r requirements.txt
```

See *configure/installation_instructions.txt* for more information on dependencies.

# Quick Start

All commands can be run from the project root using `make`. Run `make help` to see all available commands.

### Full pipeline (raw .pcap to model)

```
make preprocess PCAP=your_file.pcap
make train CSV=your_file.csv MODEL=my_model.json
```

### Using pre-split test data

Extract the test pcap data:

```
cd data/pcap
tar -xzf friday_32_pcaps.tar.gz
cd ../..
```

Run nprint and generate the CSV:

```
make nprint
make csv CSV=output.csv
```

Train a new model or test with the pre-trained one:

```
make train CSV=output.csv MODEL=my_model.json
make test MODEL=friday_model.json CSV=output.csv
```

# Overview

There are two phases to OsirisML - **preprocessing** and **ML application**.

## Preprocessing

The preprocessing pipeline converts raw .pcap files into labeled CSV data. It can be run as a single command:

```
make preprocess PCAP=your_file.pcap
```

Or as individual steps:

1. **tcp_dump.sh** - Splits a .pcap file by source IP and labels each split with its OS. Source IPs and OS labels must be configured in *preprocessing/tcp_dump.sh*.

   https://www.tcpdump.org/

2. **nprint.sh** - Converts all .pcap files in *data/pcap/pcap_os_split/* to tabular .npt files in *data/npt/* using the nPrint tool.

   ```
   make nprint
   ```

   https://github.com/nprint/nprint

   Note: OsirisML is configured to work with *nprint-1.2.1*. To use a newer version, see nprint's GitHub for installation instructions and replace the tar file in *configure/*.

3. **npt_to_csv.py** - Combines all .npt files into a single labeled CSV file in *data/csv/*.

   ```
   make csv CSV=output.csv
   ```

## Machine Learning Application

All model scripts are in the *model/* directory. Trained models are saved to *model/json/*. Feature importance plots are saved to *model/feature_importance/*.

1. **xgboostmodel.py** - Trains an XGBoost classifier on the labeled CSV data and generates feature importance plots.

   ```
   make train CSV=data.csv MODEL=modelname.json
   ```

   An optional test split size (default 0.2) can be passed when running directly:

   ```
   cd model
   python3 xgboostmodel.py data.csv modelname.json 0.3
   ```

2. **hyperparameter_tuning.py** - Searches for optimal XGBoost parameters for a given dataset.

   ```
   make tune CSV=data.csv
   ```

   Modify the `param_grid` in the script to specify which parameters to search. Complex grids require significant time and resources.

   See https://xgboost.readthedocs.io/en/stable/parameter.html for all parameters.

3. **trainmodel.py** - Retrains an existing model on additional CSV data.

   ```
   cd model
   python3 trainmodel.py current_model.json data.csv new_model.json
   ```

4. **testmodel.py** - Tests a model against a CSV file. This is the **passive OS fingerprinting** step.

   ```
   make test MODEL=model.json CSV=data.csv
   ```

### Dependencies

- https://xgboost.readthedocs.io/en/stable/
- https://pandas.pydata.org/
- https://scikit-learn.org/stable/

# Results with CIC-IDS2017 Dataset

Using *Friday-WorkingHours.pcap* from the [CIC-IDS-2017 dataset](http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/CIC-IDS-2017/PCAPs/) (8.2 GB, over 4.5 million samples):

- **Accuracy: 84.91%**
- **F1 Score: 82.96%**

Data split: 80% training/validation, 20% testing. Run on a VM with *Ubuntu 22.04.4* and 128 GB of RAM.

# Default OSes and Source IPs

These are the default OS labels and source IPs in *preprocessing/tcp_dump.sh*, based on the CIC-IDS2017 network topology from the University of New Brunswick:

| OS | Source IP(s) |
|---|---|
| Web server 16 Public | 192.168.10.50, 205.174.165.68 |
| Ubuntu server 12 Public | 192.168.10.51, 205.174.165.66 |
| Ubuntu 14.4, 32B | 192.168.10.19 |
| Ubuntu 14.4, 64B | 192.168.10.17 |
| Ubuntu 16.4, 32B | 192.168.10.16 |
| Ubuntu 16.4, 64B | 192.168.10.12 |
| Win 7 Pro, 64B | 192.168.10.9 |
| Win 8.1, 64B | 192.168.10.5 |
| Win Vista, 64B | 192.168.10.8 |
| Win 10, Pro 32B | 192.168.10.14 |
| Win 10, 64B | 192.168.10.15 |
| MAC | 192.168.10.25 |
| Kali | 205.174.165.73 |

To use OsirisML with a different dataset, modify *preprocessing/tcp_dump.sh* to map each source IP to its corresponding OS. This works best in a controlled environment where each source IP is a unique OS.

# Testing Data

**To test model creation:** There is a zip file in *data/csv/* that can be unzipped to retrieve a CSV for testing model generation.

**To test preprocessing:** There is a *tar.gz* file in *data/pcap/* with 13 pre-split pcap files (one per OS). Extract with:

```
cd data/pcap
tar -xzf friday_32_pcaps.tar.gz
```

The files will be placed into *data/pcap/pcap_os_split/*, where the preprocessing scripts expect them.
