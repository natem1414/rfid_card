from threading import Thread
import time
import serial
import RPi.GPIO as GPIO
import datetime
import socket
import os
import commands
import logging
import logging



weekdayactive = '12-45637'
curr_weekday = datetime.datetime.today().isoweekday()
curr_weekday = str(weekday)

if any((c in weekdayactive) for c in curr_weekday):
    print('Found')
else:
    print('Not Found')
