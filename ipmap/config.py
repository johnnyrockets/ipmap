#!/usr/bin/env python
import os


HOME_DIR = os.path.expanduser('~')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


#
# The MaxMind geo ip database which was obtained here:
# http://dev.maxmind.com/geoip/geoip2/geolite2/
# more specifically, here:
# http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
#
GEO_DB = os.path.join(HOME_DIR, 'Copy/Tools/geolite/GeoLite2-City.mmdb')


#
# The output from the script will be saved here.
# This can be overridden using the script args, such as:
# python ipmap.py -o /path/to/new/location/ipmap.json
# for https://johnbiz.net/tools/ip-map/
#
OUTPUT_FILE = os.path.join(BASE_DIR, 'output', 'johnbiz_ipmap.json')


#
# The logfile
#
LOG_FILE = os.path.join(BASE_DIR, 'log', 'ipmap.log')