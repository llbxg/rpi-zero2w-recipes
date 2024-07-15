#!/bin/bash

# Usage:
# The script enables or disables services based on command line options.
# Usage: $(basename $0) [-n] [-d] [-t] [-v]

set -euo pipefail

NETWORK=0
DNS=0
NTP=0
VERBOSE=0

# Function for verbose output
verbose_echo() {
  if [ $VERBOSE -eq 1 ]; then
    echo "$@"
  fi
}

while getopts "ndtvh" opt; do
  case ${opt} in
    n ) NETWORK=1 ;;
    d ) DNS=1 ;;
    t ) NTP=1 ;;
    v ) VERBOSE=1 ;;
    h )
      echo "Usage: $(basename "$0") [-n] [-d] [-t] [-v]"
      echo "-n: Enable network management (systemd-networkd)"
      echo "-d: Enable DNS resolving (systemd-resolved)"
      echo "-t: Enable NTP client (systemd-timesyncd)"
      echo "-v: Enable verbose output"
      exit 0
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
  esac
done

# Enable network management
if [ $NETWORK -eq 1 ]; then
  verbose_echo "Enabling network management..."
  systemctl enable systemd-networkd
fi

# Enable DNS resolving
if [ $DNS -eq 1 ]; then
  verbose_echo "Enabling DNS resolving..."
  cat <<EOF > /etc/systemd/resolved.conf
[Resolve]
DNS=8.8.8.8 8.8.4.4
FallbackDNS=1.1.1.1 1.0.0.1
Domains=example.com
LLMNR=yes
MulticastDNS=yes
DNSSEC=no
Cache=yes
DNSStubListener=yes
EOF
  systemctl enable systemd-resolved
  if ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf; then
    verbose_echo "Symbolic link for /etc/resolv.conf has been set."
  else
    echo "Failed to create symbolic link for /etc/resolv.conf" >&2
    exit 1
  fi
fi

# Enable NTP client
if [ $NTP -eq 1 ]; then
  verbose_echo "Enabling NTP client..."
  systemctl enable systemd-timesyncd
fi
