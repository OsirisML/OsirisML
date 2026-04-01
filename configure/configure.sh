#!/bin/bash

set -e

# Resolve the project root relative to this script's location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Function to install nprint
install_nprint() {
    if command -v nprint &> /dev/null; then
        echo "nprint is already installed, skipping."
        return
    fi

    echo "Installing nprint dependencies..."
    apt-get install -y libpcap-dev g++ make

    echo "Building nprint..."
    cd "$SCRIPT_DIR"

    # See https://github.com/nprint/nprint to download a different version
    tar -xvf nprint-1.2.1.tar.gz
    cd nprint-1.2.1
    ./configure
    make
    make install
    cd "$SCRIPT_DIR"

    echo "nprint installation completed."
}

# Function to install Python dependencies
install_python_dependencies() {
    echo "Installing Python dependencies..."
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        pip install -r "$PROJECT_ROOT/requirements.txt"
    else
        echo "WARNING: requirements.txt not found, installing defaults..."
        pip install pandas scikit-learn xgboost scapy matplotlib numpy
    fi
    echo "Python dependencies installed."
}

# Create required data directories
create_directories() {
    echo "Creating data directories..."
    mkdir -p "$PROJECT_ROOT/data/npt"
    mkdir -p "$PROJECT_ROOT/data/csv"
    mkdir -p "$PROJECT_ROOT/data/pcap/pcap_os_split"
    mkdir -p "$PROJECT_ROOT/model/json"
    mkdir -p "$PROJECT_ROOT/model/feature_importance"
    echo "Directories created."
}

# Set executable permissions on preprocessing scripts
set_permissions() {
    echo "Setting script permissions..."
    chmod +x "$PROJECT_ROOT/preprocessing/nprint.sh"
    chmod +x "$PROJECT_ROOT/preprocessing/tcp_dump.sh"
    chmod +x "$PROJECT_ROOT/preprocessing/process_pcap.sh"
    echo "Permissions set."
}

# Main function
main() {
    echo "=== OsirisML Configuration ==="
    echo "Project root: $PROJECT_ROOT"
    install_nprint
    install_python_dependencies
    create_directories
    set_permissions
    echo "=== Configuration complete ==="
}

# Execute main function
main
