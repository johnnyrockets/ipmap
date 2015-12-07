#!/usr/bin/env python
import geoip2.database
import config


class GEOIPAddress(object):
    """
    A wrapper class for the geoip2 API.
    https://github.com/maxmind/GeoIP2-python
    """
    def __init__(self, ip):
        self.ip = ip
        self.count = 0
        self._data = self._get_data()

    def _get_data(self):
        """ Loads the database and gets a reader obj """
        reader = geoip2.database.Reader(config.GEO_DB)
        return reader.city(self.ip)

    @property
    def latitude(self):
        return self._data.location.latitude

    @property
    def longitude(self):
        return self._data.location.longitude

    @property
    def city(self):
        return self._data.city.name or ''

    @property
    def coordinates(self):
        return (self.latitude, self.longitude)