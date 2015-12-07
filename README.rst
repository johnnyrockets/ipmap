IPMAP
==================


.. contents:: Table of Contents

A Python 3 script to parse a packet capture file into a JSON object that can be uploaded to https://johnbiz.net/tools/ip-map/.  The JSON object is used to display each non-private IP address on a Google Map.  It's a great way to get a visual on the source and destination of your IP traffic.


Getting Started
~~~~~~~~~~~~~~~~

Obtaining a packet capture
--------------------------

This can be done a multitude of ways.  I've listed a few here.

* Using a command line tools such as tcpdump_.
* Wireshark_.
* Using built in firewall packet capture tools, such as those provided by Pfsense_.

**NOTE**: The packet capture needs to be a .pcap file, not a .pcapng.  Converting a pcapng file to pcap can be done using the tshark command (Linux).::

    tshark -r capture.pcapng -w capture.pcap -F libpcap


Installation
------------

#. Download the `MaxMind geoip2 database`_.

#. Get the code and set up the virtual environment. ::

    git clone https://github.com/johnnyrockets/ipmap
    cd ipmap/
    mkvirtualenv ipmap_env
    pip install -r requirements.txt
    cd ipmap

#. Set global variables in ``ipmap/ipmap/config.py`` file. ::

    #
    # This is the only required variable needing to be set
    # Set it to the path where you saved the GeoLite2-City.mmdb.gz file
    #
    GEO_DB = ...

#. Run the script::

    python ipmap.py -h
    python ipmap.py -i /path/to/capture.pcap

This may take some time, depending on the size of you packet capture file.  Once completed, you can visit https://johnbiz.net/tools/ip-map/ and upload the .json file.

The JSON object looks like this::

    {
      "192.161.154.1": {
        "city": "San Francisco",
        "aliases": "",
        "hostname": "proxy.vip.pod5.iad1.zdsys.com",
        "latitude": 37.7758,
        "longitude": -122.4128,
        "src": 84,
        "dst": 88
      }
    }

The resulting page will display all the IP addresses on a Google Map.

.. image:: http://johnbiz.net/static/img/ipmap_screenshot.jpg
   :alt: Google Map with IP Address markers


.. _tcpdump: https://www.wireshark.org/docs/wsug_html_chunked/AppToolstcpdump.html
.. _Wireshark: http://www.howtogeek.com/104278/how-to-use-wireshark-to-capture-filter-and-inspect-packets/
.. _Pfsense: https://doc.pfsense.org/index.php/Sniffers,_Packet_Capture
.. _MaxMind geoip2 database: http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz