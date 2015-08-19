#!/usr/bin/env python
# encoding: utf-8

# Log serial monitor data
# TO-DO: add options for serial device, baud rate

import serial
import datetime
ser = serial.Serial('/dev/cu.usbmodemfa131', 9600)

now = datetime.datetime.now()

def get_date_string():
    day = now.day
    month = now.month
    year = now.year
    current_day = "{0}-{1}-{2}".format(year, month, day)

    return current_day


while True:
    current_date = get_date_string()
    filename = current_date + '.temperature.log'
    with open(filename, 'a') as log:
        try:
            temp = ser.readline()
            #temp = 76
            now = datetime.datetime.now()
            iso = now.isoformat()
            data = "{0} {1}".format(iso, temp)
            print data.strip()
            log.write(data)
            #print now, temp
        except:
            pass
