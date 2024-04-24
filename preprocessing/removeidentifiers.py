import sys
import pandas as pd

usage_message = "Usage: python3 <this script.py> <npt file to modify> <name of new npt file>"

if len(sys.argv) != 3:
    print(usage_message)
    sys.exit(1)

print(f"Loading {sys.argv[1]}")
try:
    df = pd.read_csv(f"../data/npt/{sys.argv[1]}")
    print("npt file loaded")
except FileNotFoundError:
    print(f"Error: File '{sys.argv[1]}' not found")
except Exception as e:
    print(f"Error: {e}")

    # mark the byte ranges to remove to avoid data leakage from overfitting source IP
ipv4_source_start, ipv4_source_end = 97, 129
ipv4_destination_start, ipv4_destination_end = 130, 160
ipv4_identification_start, ipv4_identification_end = 33, 48

tcp_source_port_start, tcp_source_port_end = 480, 496
tcp_destination_port_start, tcp_destination_port_end = 496, 512
tcp_sequence_start, tcp_sequence_end = 512, 544
tcp_ack_start, tcp_ack_end = 544, 576

# Combine all ranges to remove, including the first column (index 0)
columns_to_remove = [0] + \
    list(range(ipv4_source_start, ipv4_source_end + 1)) + \
    list(range(ipv4_destination_start, ipv4_destination_end + 1)) + \
    list(range(ipv4_identification_start, ipv4_identification_end + 1)) + \
    list(range(tcp_source_port_start, tcp_source_port_end + 1)) + \
    list(range(tcp_destination_port_start, tcp_destination_port_end + 1)) + \
    list(range(tcp_sequence_start, tcp_sequence_end + 1)) + \
    list(range(tcp_ack_start, tcp_ack_end + 1))

# Adjusting for removal from a DataFrame where columns are referenced by their integer location

df.drop(df.columns[columns_to_remove], axis=1, inplace=True)
df.to_csv(f"../data/npt/{sys.argv[2]}", index=format)
print(f"{sys.argv} saved in npt directory")
