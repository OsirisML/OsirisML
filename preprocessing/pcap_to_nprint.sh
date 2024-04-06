#!/bin/bash

# Directory where your pcap files are located
pcap_directory="../data/pcap"  # Assuming pcap files are in the same directory as the script

# Directory where you want to save the nprint output files
output_directory="../data/npt"  # Assuming you want to save output files in the data directory

# Loop through all .pcap files in the directory
for pcap_file in "$pcap_directory"/*.pcap; do
	# Check if the file exists
	if [[ -f "$pcap_file" ]]; then
		# Extract the base name without the extension
		base_name=$(basename -- "$pcap_file" .pcap)

		# Use nprint to convert pcap to its format, preserving the original file name
		# Adjust the command according to your nprint syntax and options
		nprint -P "$pcap_file" -W "$output_directory/${base_name}.npt" -4 -t
	else
		echo "File does not exist: $pcap_file"
	fi
done
