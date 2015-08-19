#!/usr/bin/env python
# encoding: utf-8

# This script reads a conf file containing an api key, city, and state abbrev.
# It prints out the observation time and temperature in Fahrenheit. You must
# have a valid Wunderground API key http://www.wunderground.com/api

import json
import urllib2
import time
import datetime
import email.utils
from sys import argv
from ConfigParser import SafeConfigParser


def read_conf(config_file):
    """Read config file"""

    config = SafeConfigParser()
    config.read(config_file)
    api_key = config.get('weather', 'api_key')
    state = config.get('weather', 'state_abbv')
    city = config.get('weather', 'city').replace(' ', '_')
    values = {'key': api_key, 'state': state, 'city': city}

    return values


def get_weather(values):
    """Call wundergroup api to get
    current outside weather"""

    url = 'http://api.wunderground.com/api/{0}/geolookup/conditions/q/{1}/{2}.json'
    api_key = values['key']
    city = values['city']
    state = values['state']
    url = url.format(api_key, state, city)
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    temp_f = parsed_json['current_observation']['temp_f']
    rfc_time = parsed_json['current_observation']['observation_time_rfc822']
    rfc_tuple = email.utils.parsedate_tz(rfc_time)
    utc_time = email.utils.mktime_tz(rfc_tuple)
    isotime = datetime.datetime.fromtimestamp(utc_time).isoformat()
    f.close()

    return (isotime, temp_f)


def main():
    conf_file = argv[1]
    conf_data = read_conf(conf_file)
    isotime, temp_f = get_weather(conf_data)
    print isotime, temp_f


if __name__ == "__main__":
    main()
