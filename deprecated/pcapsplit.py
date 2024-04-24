from scapy.all import PcapReader, PcapWriter  # Imports PcapReader and PcapWriter classes from Scapy for reading and writing PCAP files.
import math  # Imports the math library for mathematical operations.
import os  # Imports the os library for interacting with the operating system, like handling file paths.

def split_pcap_file(pcap_file, parts=4):  # Defines a function to split a PCAP file into a specified number of parts, defaulting to 4.
    packets = list(PcapReader(pcap_file))  # Reads all packets from the input PCAP file into a list using Scapy's PcapReader.
    total_packets = len(packets)  # Calculates the total number of packets in the PCAP file.
    packets_per_file = math.ceil(total_packets / parts)  # Determines the number of packets per split file, rounding up to ensure all packets are included.

    for part in range(parts):  # Loops through each part (from 0 to parts-1) to create each split file.
        start_index = part * packets_per_file  # Calculates the start index for the current part.
        end_index = start_index + packets_per_file  # Calculates the end index for the current part.
        # Generates the output filename by adding "_part_X" before the file extension, where X is the part number (starting from 1).
        output_filename = f"{os.path.splitext(pcap_file)[0]}_part_{part + 1}.pcap"

        with PcapWriter(output_filename, append=True, sync=True) as writer:  # Opens a new PCAP file for writing using PcapWriter.
            for packet in packets[start_index:end_index]:  # Loops over each packet in the current part's range.
                writer.write(packet)  # Writes the current packet to the split PCAP file.

        print(f"Created {output_filename}")  # Prints a message indicating the creation of a split PCAP file.

# Example usage
pcap_file = 'example.pcap'  # Specifies the path to the PCAP file to be split.
split_pcap_file(pcap_file)  # Calls the function to split the specified PCAP file into parts.
