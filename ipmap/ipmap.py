#!/usr/bin/env python
import argparse
import ipaddress
import json
import logging
import os
import socket
import sys
import config
from datetime import datetime
from scapy.all import IP, PcapReader
from lib.ops_logger import initialize_log
from lib.geoip_address import GEOIPAddress


logger = initialize_log(config.LOG_FILE, 'packet')


def lookup(ip_address):
    """
    Perform a DNS reverse lookup on an ip address.  This
    returns a tuple of (hostname, [aliases], [ipaddrlist]).

    http://stackoverflow.com/questions/7832264#8225878
    """
    try:
        return socket.gethostbyaddr(ip_address)
    except socket.herror:
        return '', [], None


def add_ip_data(ip_dict, ip_address, target):
    """
    This function builds the ip_dict dictionary.  The
    structure looks like this:

    {"192.161.154.1": {
        "city": "San Francisco",
        "aliases": "",
        "hostname": "proxy.vip.pod5.iad1.zdsys.com",
        "latitude": 37.7758,
        "longitude": -122.4128,
        "src": 84,
        "dst": 88
        }
    }
    """
    # If this is a private IP address, don't do anything
    if ipaddress.ip_address(ip_address).is_private:
        logger.debug('SKIPPING private address')
        return
    logger.info('Processing IP: "{} {}"'.format(target, ip_address))
    geoip = GEOIPAddress(ip_address)
    hostname, aliaslist, ipaddrlist = lookup(ip_address)
    # Make sure that we have a latitude and longitude.
    if geoip.latitude and geoip.longitude:
        if ip_address not in ip_dict.keys():
            # This is a new IP Address
            ip_dict[ip_address] = {
                'city': geoip.city,
                'latitude': geoip.latitude,
                'longitude': geoip.longitude,
                'src': 0,
                'dst': 0,
                'hostname': hostname,
                'aliases': ', '.join(aliaslist),
            }
        if target == 'src':
            ip_dict[ip_address]['src'] += 1
        elif target == 'dst':
            ip_dict[ip_address]['dst'] += 1
        else:
            logger.warning('WARNING: invalid target "{}".  Should be src or dst'.format(target))
    else:
        logger.warning('MISSING latitude and/or longitude')


def get_args():
    """
    Sets up argparse and returns the arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--capture-file', help='The capture file to use.')
    parser.add_argument('-o', '--outfile', help='The output file.')
    parser.parse_args()
    return parser.parse_args()


if __name__ == '__main__':
    start_time = datetime.now()
    logger.info('Starting')
    args = get_args()
    output_file = args.outfile or config.OUTPUT_FILE
    pcapfile = args.capture_file
    if not os.path.exists(pcapfile):
        logger.error('Unable to located PCAP capture file')
        logger.error('Bad path: "{}"'.format(pcapfile))
        sys.exit(1)
    ip_dict = {}
    try:
        for packet in PcapReader(pcapfile):
            if packet.haslayer(IP):
                # Each IP packet has a source and destination,
                # so add each to the ip_data dict.
                add_ip_data(ip_dict, packet.getlayer(IP).src, 'src')
                add_ip_data(ip_dict, packet.getlayer(IP).dst, 'dst')
    finally:
        # Write the ip_dict to file
        with open(output_file, 'w') as fh:
            fh.write(json.dumps(ip_dict))
            logger.info('Output written to "{}"'.format(output_file))
        logger.info('Done: began at {}'.format(start_time.strftime('%H:%M:%S')))
