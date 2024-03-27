from scapy.all import PcapReader, PcapWriter
import math
import os

def split_pcap_file(pcap_file, parts=4):
    packets = list(PcapReader(pcap_file))
    total_packets = len(packets)
    packets_per_file = math.ceil(total_packets / parts)

    for part in range(parts):
        start_index = part * packets_per_file
        end_index = start_index + packets_per_file
        output_filename = f"{os.path.splitext(pcap_file)[0]}_part_{part + 1}.pcap"

        with PcapWriter(output_filename, append=True, sync=True) as writer:
            for packet in packets[start_index:end_index]:
                writer.write(packet)

        print(f"Created {output_filename}")

# Example usage
pcap_file = 'example.pcap'  # Update this to your PCAP file path
split_pcap_file(pcap_file)