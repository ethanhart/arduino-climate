#!/usr/bin/env python
# encoding: utf-8

# Log serial monitor data
# TO-DO: add options for serial device, baud rate

import serial
import datetime
import weather
import time
from sys import argv

ser = serial.Serial('/dev/cu.usbmodemfa131', 9600)

now = datetime.datetime.now()

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
    ser.flush()
    with open(filename, 'a') as log:
        try:
            inside_temp = ser.readline().strip()
            if len(inside_temp) < 1:
                while len(inside_temp) < 1:
                    inside_temp = ser.readline().strip()
            if time_since_log >= 20:
                wunder_isotime, outside_temp = weather.get_weather(conf_data)
                now = datetime.datetime.now()
                iso = now.isoformat()
                data = "{0} {1} {2}\n".format(iso, inside_temp, outside_temp)
                print data.strip()
                log.write(data)
                old_log_time = logtime
            else:
                print "Inside temp: {0}".format(inside_temp)
        except (KeyboardInterrupt, SystemExit):
            ser.close()
            exit()
        except:
            pass
    time.sleep(1)
