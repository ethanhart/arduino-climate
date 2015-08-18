#!/usr/bin/env python
# encoding: utf-8

# This script reads a conf file containing an api key, city, and state abbrev.
# It prints out the observation time and temperature in Fahrenheit. You must
# have a valid Wunderground API key http://www.wunderground.com/api

import json
import urllib2
import datetime
import email.utils
from sys import argv
from ConfigParser import SafeConfigParser

# Read config
config = SafeConfigParser()
config.read(argv[1])
api_key = config.get('weather', 'api_key')
state = config.get('weather', 'state_abbv')
city = config.get('weather', 'city').replace(' ', '_')

# Get json weather data
url = 'http://api.wunderground.com/api/{0}/geolookup/conditions/q/{1}/{2}.json'
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

print isotime, temp_f
f.close()
