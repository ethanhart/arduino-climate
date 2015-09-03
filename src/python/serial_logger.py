#!/usr/bin/env python
# encoding: utf-8

# Log serial monitor data
# TO-DO: add options for serial device, baud rate

import serial
import datetime
import weather
import time
from sys import argv

arduino = serial.Serial('/dev/cu.usbmodemfa131', 9600)

now = datetime.datetime.now()

delay_time = 180  # delay time to query wunderground

def get_date_string():
    day = now.day
    month = now.month
    year = now.year
    current_day = "{0}-{1}-{2}".format(year, month, day)

    return current_day

conf = argv[1]
conf_data = weather.read_conf(conf)

old_log_time = time.localtime()

while True:
    logtime = time.gmtime()
    time_since_log = (time.mktime(logtime) - time.mktime(old_log_time))
    current_date = get_date_string()
    filename = current_date + '.temperature.log'
    arduino.write('T') # ping arduino
    time.sleep(1) # wait a second to give the arduino time to read temp

    with open(filename, 'a') as log:
        try:
            inside_temp = arduino.readline().strip()
            if time_since_log >= delay_time:
                wunder_isotime, outside_temp = weather.get_weather(conf_data)
                now = datetime.datetime.now()
                iso = now.isoformat()
                data = "{0} {1} {2}\n".format(iso, inside_temp, outside_temp)
                print data.strip()
                log.write(data)
                old_log_time = logtime
            #else:
                #print "Inside temp: {0}".format(inside_temp)
        except (KeyboardInterrupt, SystemExit):
            arduino.close()
            exit()
    #with open('arduino.tmp', 'a') as ard:
        #d = "{0} {1}\n".format(iso, inside_temp)
        #ard.write(d)
    time.sleep(1)
    arduino.flush()
