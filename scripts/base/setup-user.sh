#!/bin/bash

# Usage:
# The script requires a username directly as the first argument and optionally accepts 
#   a password, verbose output, sudo group addition, and encrypted password flag.
# Usage: $(basename $0) username [-p password] [-v] [-s] [-e]

set -euo pipefail

USERNAME=$1
PASSWORD=""
VERBOSE=0
SUDO=0
ENCRYPTED=0

# Exit if no username is provided
if [ -z "$USERNAME" ]; then
  echo "Username is required as the first argument."
  exit 1
fi

shift # Shift the arguments to left so that getopts can process options starting from $1.

# Function for verbose output
verbose_echo() {
  if [ $VERBOSE -eq 1 ]; then
    echo "$@"
  fi
}

while getopts "p:vshe" opt; do
  case ${opt} in
    p ) PASSWORD=$OPTARG ;;
    v ) VERBOSE=1 ;;
    s ) SUDO=1 ;;
    e ) ENCRYPTED=1 ;;
    h )
      echo "Usage: $(basename "$0") username [-p password] [-v] [-s] [-e]"
      exit 0 ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1 ;;
    : )
      echo "Invalid option: -$OPTARG requires an argument" 1>&2
      exit 1 ;;
  esac
done

verbose_echo "Verbose mode is on."
verbose_echo "Adding user $USERNAME..."

useradd -m -s /bin/bash "$USERNAME"
verbose_echo "User $USERNAME has been added."

# Add the user to the sudo group if the -s option was provided
if [ $SUDO -eq 1 ]; then
  usermod -aG sudo "$USERNAME"
  verbose_echo "$USERNAME has been added to the sudo group."
else
  verbose_echo "$USERNAME has not been added to the sudo group."
fi

# Set the password if provided
if [ -n "$PASSWORD" ]; then
  if [ $ENCRYPTED -eq 1 ]; then
    echo "${USERNAME}:${PASSWORD}" | chpasswd -e
    verbose_echo "Encrypted password for $USERNAME has been set."
  else
    echo "${USERNAME}:${PASSWORD}" | chpasswd
    verbose_echo "Password for $USERNAME has been set."
  fi
else
  echo "$USERNAME:$USERNAME" | chpasswd  # Default password is the username
  verbose_echo "Default password set for $USERNAME."
fi

verbose_echo "User $USERNAME has been fully configured."
