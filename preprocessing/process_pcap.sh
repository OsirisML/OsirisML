#!/bin/bash

# Takes a .pcap file and runs supporting preprocessing scripts to convert to .csv

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pcap_file.pcap>"
    echo "file must be in ../data/pcap"
    exit 1
fi

filename="$1"

basename=$(basename "$1" .pcap)  # Extract filename without extension

# Runs tcp dump - make sure correct IPs and OSes are configured in tcp_dump.sh
./tcp_dump.sh $filename

# Runs nprint in the ../data/pcap/pcap_os_split directory and outputs to ../data/npt
./nprint.sh

# Concatenates the .npt files to a single .csv and adds labels
python3 "lisanalgaib.py" "$basename.csv"
