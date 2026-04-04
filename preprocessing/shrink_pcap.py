import argparse
import os
import random
import struct

PCAPNG_SHB = 0x0A0D0D0A  # Section Header Block
PCAPNG_IDB = 0x00000001  # Interface Description Block
PCAPNG_EPB = 0x00000006  # Enhanced Packet Block
PCAPNG_SPB = 0x00000003  # Simple Packet Block


def read_block(f, endian='<'):
    """Read a single pcapng block. Returns (block_type, raw_block_bytes) or (None, None) at EOF."""
    block_type_raw = f.read(4)
    if len(block_type_raw) < 4:
        return None, None

    block_type = struct.unpack(f'{endian}I', block_type_raw)[0]
    block_len_raw = f.read(4)
    if len(block_len_raw) < 4:
        return None, None

    block_len = struct.unpack(f'{endian}I', block_len_raw)[0]
    # Read remaining block data (block_len includes the type and length fields we already read,
    # plus a trailing copy of block_len)
    remaining = block_len - 8
    if remaining < 0:
        return None, None
    rest = f.read(remaining)
    if len(rest) < remaining:
        return None, None

    raw_block = block_type_raw + block_len_raw + rest
    return block_type, raw_block


def shrink_pcapng(pcap_file, fraction, seed=42):
    file_size = os.path.getsize(pcap_file)
    print(f"Input file: {pcap_file}")
    print(f"Input size: {file_size / (1024**3):.2f} GB")
    print(f"Target: 1/{fraction} of packets (randomly sampled)")

    # First pass: count packet blocks
    print("\nPass 1: Counting packets...")
    packet_count = 0
    with open(pcap_file, 'rb') as f:
        while True:
            block_type, raw = read_block(f)
            if block_type is None:
                break
            if block_type in (PCAPNG_EPB, PCAPNG_SPB):
                packet_count += 1
            if packet_count % 1_000_000 == 0 and packet_count > 0:
                print(f"  Counted {packet_count:,} packets so far...")

    keep_count = packet_count // fraction
    print(f"Total packets: {packet_count:,}")
    print(f"Keeping: {keep_count:,} packets")

    # Generate random indices to keep
    random.seed(seed)
    keep_indices = set(random.sample(range(packet_count), keep_count))

    # Second pass: write selected packets (keep all non-packet blocks like SHB, IDB)
    output_filename = f"{os.path.splitext(pcap_file)[0]}_half.pcap"
    print(f"\nPass 2: Writing to {output_filename}...")

    written = 0
    pkt_idx = 0
    with open(pcap_file, 'rb') as fin, open(output_filename, 'wb') as fout:
        while True:
            block_type, raw = read_block(fin)
            if block_type is None:
                break

            if block_type in (PCAPNG_EPB, PCAPNG_SPB):
                if pkt_idx in keep_indices:
                    fout.write(raw)
                    written += 1
                    if written % 500_000 == 0:
                        print(f"  Written {written:,} / {keep_count:,} packets...")
                pkt_idx += 1
            else:
                # Always keep metadata blocks (SHB, IDB, etc.)
                fout.write(raw)

    output_size = os.path.getsize(output_filename)
    print(f"\nDone! Written {written:,} packets")
    print(f"Output size: {output_size / (1024**3):.2f} GB")
    print(f"Reduction: {(1 - output_size / file_size) * 100:.1f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shrink a PCAP/PCAPNG file by randomly sampling packets")
    parser.add_argument("pcap_file", type=str, help="Path to the input PCAP file")
    parser.add_argument("--fraction", type=int, default=2, help="Divisor for packet count (default: 2 = half)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")
    args = parser.parse_args()

    shrink_pcapng(args.pcap_file, args.fraction, args.seed)
