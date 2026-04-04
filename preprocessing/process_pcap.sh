#!/bin/bash

set -e

# Resolve paths relative to this script's location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Takes a .pcap file and runs supporting preprocessing scripts to convert to .csv

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pcap_file.pcap>"
    echo "File must be in $PROJECT_ROOT/data/pcap/"
    exit 1
fi

filename="$1"
basename=$(basename "$1" .pcap)

echo "=== Processing $filename ==="

# Runs tcp dump - make sure correct IPs and OSes are configured in tcp_dump.sh
echo "Step 1/3: Running tcpdump to split by OS..."
"$SCRIPT_DIR/tcp_dump.sh" "$filename"

# Runs nprint on the split pcap files
echo "Step 2/3: Running nprint..."
"$SCRIPT_DIR/nprint.sh"

# removes the split .pcap files that are no longer needed
rm -rf "$PROJECT_ROOT/data/pcap/pcap_os_split/"

# Concatenates the .npt files to a single .csv and adds labels
echo "Step 3/3: Converting to CSV..."
cd "$SCRIPT_DIR"
python3 npt_to_csv.py "$basename.csv"

# removes the .npt files that are no longer needed
rm -rf "$PROJECT_ROOT/data/npt/"

echo "=== Processing complete ==="
echo "CSV output: $PROJECT_ROOT/data/csv/$basename.csv"
echo "Use model scripts to generate, retrain, and test models from this CSV."
