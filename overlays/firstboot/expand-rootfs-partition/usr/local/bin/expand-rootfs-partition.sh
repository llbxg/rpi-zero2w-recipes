#!/bin/bash

# This script resizes the partition and filesystem, then removes itself.

set -euo pipefail

# Default values
DEVICE="/dev/mmcblk0"
PARTITION="2"
ROOT_PART="${DEVICE}p${PARTITION}"
VERBOSE=0
REMOVE_TOOLS=0
REMOVE_SCRIPT=0

# Function for verbose output
verbose_echo() {
  if [ $VERBOSE -eq 1 ]; then
    echo "$@"
  fi
}

# Usage message
usage() {
  echo "Usage:"
  echo "  $(basename "$0") -d DEVICE -p PARTITION [-v] [-r] [-s]"
  echo "Options:"
  echo "  -d DEVICE      Specify the device (default: /dev/mmcblk0)"
  echo "  -p PARTITION   Specify the partition number (default: 2)"
  echo "  -v             Enable verbose output"
  echo "  -r             Remove parted and fdisk after resizing"
  echo "  -s             Remove script and disable service after resizing"
  exit 1
}

# Parse command line options
while getopts "d:p:vrs" opt; do
  case ${opt} in
    d ) DEVICE=$OPTARG ;;
    p ) PARTITION=$OPTARG ;;
    v ) VERBOSE=1 ;;
    r ) REMOVE_TOOLS=1 ;;
    s ) REMOVE_SCRIPT=1 ;;
    \? ) usage ;;
  esac
done

# Update ROOT_PART based on provided DEVICE and PARTITION
ROOT_PART="${DEVICE}p${PARTITION}"

verbose_echo "Starting the partition and filesystem expansion process..."

verbose_echo "Resizing the partition ${PARTITION} on ${DEVICE}..."
sudo parted "${DEVICE}" resizepart "${PARTITION}" 100%

verbose_echo "Resizing the filesystem on ${ROOT_PART}..."
sudo resize2fs "${ROOT_PART}"

if [ $REMOVE_TOOLS -eq 1 ]; then
  verbose_echo "Removing parted and fdisk..."
  sudo apt-get remove --purge -y parted fdisk
else
  verbose_echo "Skipping removal of parted and fdisk."
fi

if [ $REMOVE_SCRIPT -eq 1 ]; then
  verbose_echo "Disabling service and removing script..."
  sudo systemctl disable expand-root-partition.service
  
  # Remove the script itself
  SCRIPT_PATH=$(realpath "$0")
  sudo rm -- "$SCRIPT_PATH"
  verbose_echo "Script removed: $SCRIPT_PATH"
else
  verbose_echo "Skipping removal of script and service."
fi

verbose_echo "Expansion process completed."
