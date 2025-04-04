#!/bin/bash
ip addr add 192.168.2.2/24 dev usb0
ip link set usb0 up