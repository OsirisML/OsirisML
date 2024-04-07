#!/bin/bash

# loops through a directory and runs nprint on all the .pcap files to generate .npt files

# Directory where pcap files are located - by default is ../data/pcap/os_split
pcap_directory="../data/pcap/pcap_os_split"  # Assuming pcap files are in the same directory as the script

# Directory where you want to save the nprint output files
output_directory="../data/npt/npt_os_split"  # Assuming you want to save output files in the data directory

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through all .pcap files in the directory
for pcap_file in "$pcap_directory"/*.pcap; do
	# Check if the file exists
	if [[ -f "$pcap_file" ]]; then
		# Extract the base name without the extension
		base_name=$(basename -- "$pcap_file" .pcap)

		# Use nprint to convert pcap to its format, preserving the original file name
		# Adjust the command according to your nprint syntax and options
		nprint -P "$pcap_file" -W "$output_directory/${base_name}.npt" -4 -t
		echo "nprint successful for file $pcap_file\n"
	else
		echo "File does not exist: $pcap_file"
	fi
done

echo "nprint complete to $output_directory"
