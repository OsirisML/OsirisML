#!/bin/bash

set -e

# Resolve paths relative to this script's location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Directory where pcap files are located
pcap_directory="$PROJECT_ROOT/data/pcap/pcap_os_split"

# Directory where you want to save the nprint output files
output_directory="$PROJECT_ROOT/data/npt"

# Create output directory if it doesn't exist
mkdir -p "$output_directory"

# Check that nprint is installed
if ! command -v nprint &> /dev/null; then
    echo "ERROR: nprint is not installed. Run 'sudo ./configure/configure.sh' first."
    exit 1
fi

# Check that pcap directory has files
if ! ls "$pcap_directory"/*.pcap 1> /dev/null 2>&1; then
    echo "ERROR: No .pcap files found in $pcap_directory"
    exit 1
fi

echo "Beginning nprint on .pcap files in $pcap_directory"

# Loop through all .pcap files in the directory
for pcap_file in "$pcap_directory"/*.pcap; do
    if [[ -f "$pcap_file" ]]; then
        base_name=$(basename -- "$pcap_file" .pcap)
        echo "Processing $base_name..."

        if nprint -P "$pcap_file" -W "$output_directory/${base_name}.npt" -4 -t; then
            echo "nprint successful for $base_name"
        else
            echo "ERROR: nprint failed for $pcap_file"
            exit 1
        fi
    fi
done

echo "nprint complete. Output in $output_directory"
