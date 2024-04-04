#!/bin/bash

# Check if filename parameter is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"
base_filename="${filename%.*}" # Extracting the base filename without extension

# Execute tcpdump commands
tcpdump -r "$filename" -w "${base_filename}_ubuntu-14.4-32b.pcap" src 192.168.10.19
tcpdump -r "$filename" -w "${base_filename}_ubuntu-14.4-64b.pcap" src 192.168.10.17
tcpdump -r "$filename" -w "${base_filename}_ubuntu-16.4-32b.pcap" src 192.168.10.16
tcpdump -r "$filename" -w "${base_filename}_ubuntu-16.4-64b.pcap" src 192.168.10.12
tcpdump -r "$filename" -w "${base_filename}_windows-7-pro.pcap" src 192.168.10.9
tcpdump -r "$filename" -w "${base_filename}_windows-8.1.pcap" src 192.168.10.5
tcpdump -r "$filename" -w "${base_filename}_windows-vista.pcap" src 192.168.10.8
tcpdump -r "$filename" -w "${base_filename}_windows-10-pro.pcap" src 192.168.10.14
tcpdump -r "$filename" -w "${base_filename}_windows-10.pcap" src 192.168.10.15
tcpdump -r "$filename" -w "${base_filename}_windows_mac-os-x.pcap" src 192.168.10.25
tcpdump -r "$filename" -w "${base_filename}_mac_mac-os-x.pcap" src 192.168.10.25
tcpdump -r "$filename" -w "${base_filename}_ubuntu-ubuntu-server.pcap" '(src 192.168.10.51 or src 205.174.165.66)'
tcpdump -r "$filename" -w "${base_filename}_ubuntu-web-server.pcap" '(src 192.168.10.50 or src 205.174.165.68)'
