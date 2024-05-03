#!/bin/bash

# Function to install nprint
install_nprint() {
    echo "Installing nprint..."
    apt-get install libpcap-dev
    apt install g++
    apt install make

    # See https://github.com/nprint/nprint to download a different version
    tar -xvf nprint-1.2.1.tar.gz
    cd nprint-1.2.1
    ./configure
    make
    make install
    cd ..
    echo "nprint installation completed."
}

# Function to install Python dependencies for xgboostmodel.py
install_python_dependencies() {
    echo "Installing Python dependencies..."
    apt install python3
    apt install python3-pip
    pip install pandas scikit-learn xgboost scapy
    echo "Python dependencies installed."
}

# Main function
main() {
    install_nprint
    install_python_dependencies

    # add executable permission to preprocessing scripts
    chmod +x ../preprocessing/nprint.sh
    chmod +x ../preprocessing/tcp_dump.sh
    chmod +x ../preprocessing/process_pcap.sh
}

# Execute main function
main
