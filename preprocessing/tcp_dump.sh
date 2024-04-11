#!/bin/bash

# takes a .pcap file and splits it into different .pcap files for each OS

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pcap_file.pcap>"
    exit 1
fi

filename="$1"
path_to_dir="../data/pcap"
output_dir="../data/pcap/pcap_os_split"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Execute tcpdump commands and save output to the partition directory
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/ubuntu-14.4-32b.pcap" src 192.168.10.19
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/ubuntu-14.4-64b.pcap" src 192.168.10.17
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/ubuntu-16.4-32b.pcap" src 192.168.10.16
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/ubuntu-16.4-64b.pcap" src 192.168.10.12
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/windows-7-pro.pcap" src 192.168.10.9
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/windows-8.1.pcap" src 192.168.10.5
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/windows-vista.pcap" src 192.168.10.8
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/windows-10-pro.pcap" src 192.168.10.14
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/windows-10.pcap" src 192.168.10.15
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/windows_mac-os-x.pcap" src 192.168.10.25
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/mac_mac-os-x.pcap" src 192.168.10.25
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/ubuntu-ubuntu-server.pcap" '(src 192.168.10.51 or src 205.174.165.66)'
tcpdump -r "$path_to_dir/$filename" -w "$output_dir/ubuntu-web-server.pcap" '(src 192.168.10.50 or src 205.174.165.68)'

echo "tcp dump complete to $output_dir"
