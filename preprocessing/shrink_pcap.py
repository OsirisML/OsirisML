import argparse
import os
import math
from scapy.all import PcapReader, PcapWriter

def shrink_pcap_file(pcap_file, fraction):
    packets = list(PcapReader(pcap_file))
    total_packets = len(packets)
    packets_to_extract = math.ceil(total_packets / fraction)
    output_filename = f"{os.path.splitext(pcap_file)[0]}_fraction_{fraction}.pcap"

    with PcapWriter(output_filename, append=False, sync=True) as writer:
        for packet in packets[:packets_to_extract]:
            writer.write(packet)

    print(f"Created {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shrink a PCAP file to a fraction")
    parser.add_argument("pcap_file", type=str, help="Path to the input PCAP file")
    parser.add_argument("--fraction", type=int, default=10, help="Fraction size (default: 10)")
    args = parser.parse_args()

    shrink_pcap_file(args.pcap_file, args.fraction)
