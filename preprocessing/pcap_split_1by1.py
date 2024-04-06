from scapy.all import PcapReader, PcapWriter
import math
import os

def split_pcap_file(pcap_file, parts=4):
    # First, determine the total number of packets to calculate packets per file
    total_packets = 0
    with PcapReader(pcap_file) as reader:
        for _ in reader:
            total_packets += 1

    packets_per_file = math.ceil(total_packets / parts)

    # Now, iterate again to write packets to separate files
    current_part = 0
    current_packet = 0
    writer = None
    for packet in PcapReader(pcap_file):
        # If we have written the required number of packets, or if this is the first packet
        if current_packet % packets_per_file == 0:
            if writer:  # Close the previous writer if it exists
                writer.close()
            output_filename = f"{os.path.splitext(pcap_file)[0]}_part_{current_part + 1}.pcap"
            writer = PcapWriter(output_filename, append=True, sync=True)
            print(f"Creating {output_filename}")
            current_part += 1
        
        writer.write(packet)
        current_packet += 1

    if writer:  # Make sure the last writer is closed
        writer.close()

# Example usage
pcap_file = 'example.pcap'  # Update this to your PCAP file path
split_pcap_file(pcap_file)
