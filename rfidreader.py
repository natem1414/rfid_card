## Place in /usr/local/bin/rfid/rfidreader.py

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

#LOG FILE LOCATION
logfilename= "/var/log/rfidreader.log"
logging.basicConfig(level=logging.DEBUG, filename=logfilename, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.info('+++++++++++++++++++++++++++++RFID reader script started++++++++++++++++++++++++++++')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)

def processID(ID,doornum):
  logging.debug('-=-=-=-=-=-=-=-=-=-=-=-=-=-=Entered ProcessID Function=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
  blinknumnotau = 6
  blinknum = 0
  cardmatch = 0
  IDlength = len(str(ID))
  DOORopentime = 5
  logging.debug('IDlength=%s', IDlength)
  logging.debug('ID as a HEX=%s', ID)
  print ID
#  print IDlength

#Address for sending TCP command
  TCP_IP = '192.168.4.216'
#Port for sending TCP command
  TCP_PORT = 4242
	
#set Door number
  DOORgpo = doornum + 4
  ERRORgpo = 4
  doornum = str(doornum)
  doornum = "0" + doornum
  cardfilename = "/usr/local/bin/rfid/card%s.txt" % doornum


  logging.debug('cardfilename=%s', cardfilename)
  logging.debug('DOORgpo=%s', DOORgpo)

#  print 'DOORgpo: ', DOORgpo
  BUFFER_SIZE = 1024
  authrequire = 4
  authcount = 0

  try:
    ID = str(int(ID[2:-2], 16))
    logging.debug('I was able to convert ID to what i need.  ID=%s', ID)
  except:
    ID = "2600B2E7E4"
    ID = str(int(ID[2:-2], 16))
    logging.debug('I was NOT able to convert ID to what i need so i make it up.  ID=%s', ID)

#get current time
  date_time = datetime.datetime.now()
  curr_time = datetime.datetime.now().time()
#get current weekday
  curr_weekday = datetime.datetime.today().isoweekday()
  curr_weekday = str(curr_weekday)



#  print 'date_time: ', date_time
#  print 'Current time: ', curr_time
#  print 'Door: ', doornum, 'ID: ', ID
  logging.debug('date_time=%s', date_time)
#  logging.debug('curr_time=%s', curr_time)
  logging.debug('doornum=%s', doornum)



  with open(cardfilename) as myFile:
#    print 'Card Checked'
    logging.debug('Card ID was checked.  ID=%s', ID)

    for num, line in enumerate(myFile, 1):
      if ID in line:
#        print 'found at line:', num
        logging.debug('ID Found at line: %s', num)
        foundline = line
        foundline = foundline[:-1]
#        print 'Line: ', line
        logging.debug('Line that was found: %s', foundline)
#        print 'foundline: ', foundline
        linesplit = foundline.split(";")
        logging.debug('Line Split= %s', linesplit)
#        print 'Line Split: ', linesplit
#        print 'Line Split[0]: ', linesplit[0]
#        print 'Line Split[1]: ', linesplit[1]
#        print 'Line Split[2]: ', linesplit[2]
#        print 'Line Split[3]: ', linesplit[3]
#        print 'Line Split[4]: ', linesplit[4]
#        print 'Line Split[5]: ', linesplit[5]
#        print 'Line Split[6]: ', linesplit[6]
        cardname = linesplit[0]
        cardnumber = linesplit[1]
        datestart = linesplit[2]
        dateend = linesplit[3]
	weekdayactive = linesplit[4]
        activetimestart = linesplit[5]
        activetimeend = linesplit[6]
        cardgroupnum = linesplit[7]
        datestart = datetime.datetime.strptime(datestart,"%Y-%m-%d")
        dateend = datetime.datetime.strptime(dateend,"%Y-%m-%d")
        activetimestart = datetime.datetime.strptime(activetimestart,"%H:%M").time()
        activetimeend = datetime.datetime.strptime(activetimeend,"%H:%M").time()
#        print 'datestart: ', datestart
#        print 'dateend: ', dateend
#        print 'activetimestart: ', activetimestart
#        print 'activetimeend: ', activetimeend
        if datestart < date_time < dateend:
#          print "start/end date match"
          logging.info('Start/end date match for ID %s', ID)
          authcount +=1

        if any((c in weekdayactive) for c in curr_weekday):
          logging.info('Authorized for today: %s', weekdayactive)
          authcount +=1
        else:
          logging.info('NOT Authorized for today: %s', weekdayactive)

        if activetimestart < activetimeend:
          if curr_time >= activetimestart and curr_time <= activetimeend:
#            print "active times match"
            logging.info('Active Times Match for ID %s', ID)
            authcount +=1
        else:
          if curr_time >= activetimestart or curr_time <= activetimeend:
#            print "active times match (reversed)"
            logging.info('Active Times Match when reversed for ID %s', ID)
            authcount +=1
        if ID == cardnumber:
          cardmatch = 1
          authcount +=1
        if authcount == authrequire:
#          print "Card Authorized"
          logging.info('Access is Authorized for door number %s', doornum)
          logging.info('Access is Authorized for ID %s', ID)
 
          try:
            logging.debug('Im going to try to send the command to open the door')
            tcpmessage = 'DOOR;' + doornum + ';UNLOCK_MOMENTARY;' + cardname + ';' + cardnumber + ';GROUP;' + cardgroupnum + '\n'
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(tcpmessage)
            time.sleep(0.5)
            s.close()
#            print "Done Sending Command"
            logging.info('Succeeded in sending the command, door should have opened')
          except:
#            print "Was not able to send TCP, opening door by GPO"
            logging.warning('Command Errored out, using GPO number %s', DOORgpo)
            GPIO.output(DOORgpo,GPIO.HIGH)
            time.sleep(DOORopentime)
            GPIO.output(DOORgpo,GPIO.LOW)

        else:
#          print "NOT AUTHORIZED"
          logging.warning('Card ID is not autherized for this door (possibly do to current time).')
          logging.warning('ID=%s', ID)
          logging.warning('Door=%s', doornum)
          while blinknum < blinknumnotau:
            GPIO.output(ERRORgpo,GPIO.HIGH)
            time.sleep(0.1)
	    GPIO.output(ERRORgpo,GPIO.LOW)
            time.sleep(0.1)
            blinknum = blinknum + 1
	  return

#        print 'authcount: ', authcount
  if cardmatch == 1:
#    print "Card Matched"
    logging.info('The ID was matched. ID=%s', ID)
  else:
#    print "Card Not Matched"
    logging.warning('The ID was NOT matched. ID=%s', ID)
    blinknum = 0
    while blinknum < blinknumnotau:
      GPIO.output(ERRORgpo,GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(ERRORgpo,GPIO.LOW)
      time.sleep(0.1)
      blinknum = blinknum + 1
  return

def rfid01():
	global flag
	PortRF1 = serial.Serial('/dev/ttyUSB0',9600)
	DOOR = 01
	while True:
        	ID = ""
        	read_byte1 = PortRF1.read()
        	if read_byte1=="\x02":
                	for Counter in range(12):
                        	read_byte1=PortRF1.read()
                        	ID = ID + str(read_byte1)
			processID(ID,DOOR)
def rfid02():
	global flag
	PortRF2 = serial.Serial('/dev/ttyUSB1',9600)
	DOOR = 02
	while True:
        	ID = ""
        	read_byte2 = PortRF2.read()
        	if read_byte2=="\x02":
                	for Counter in range(12):
                        	read_byte2=PortRF2.read()
                        	ID = ID + str(read_byte2)
			processID(ID,DOOR)
def rfid03():
	global flag
	PortRF1 = serial.Serial('/dev/ttyUSB2',9600)
	DOOR = 03
	while True:
        	ID = ""
        	read_byte1 = PortRF1.read()
        	if read_byte1=="\x02":
                	for Counter in range(12):
                        	read_byte1=PortRF1.read()
                        	ID = ID + str(read_byte1)
			processID(ID,DOOR)
def rfid04():
	global flag
	PortRF1 = serial.Serial('/dev/ttyUSB3',9600)
	DOOR = 04
	while True:
        	ID = ""
        	read_byte1 = PortRF1.read()
        	if read_byte1=="\x02":
                	for Counter in range(12):
                        	read_byte1=PortRF1.read()
                        	ID = ID + str(read_byte1)
			processID(ID,DOOR)
def rfid05():
	global flag
	PortRF1 = serial.Serial('/dev/ttyUSB4',9600)
	DOOR = '05'
	while True:
        	ID = ""
        	read_byte1 = PortRF1.read()
        	if read_byte1=="\x02":
                	for Counter in range(12):
                        	read_byte1=PortRF1.read()
                        	ID = ID + str(read_byte1)
			processID(ID,DOOR)
def rfid06():
	global flag
	PortRF1 = serial.Serial('/dev/ttyUSB5',9600)
	DOOR = '06'
	while True:
        	ID = ""
        	read_byte1 = PortRF1.read()
        	if read_byte1=="\x02":
                	for Counter in range(12):
                        	read_byte1=PortRF1.read()
                        	ID = ID + str(read_byte1)
			processID(ID,DOOR)
def rfid07():
	global flag
	PortRF1 = serial.Serial('/dev/ttyUSB6',9600)
	DOOR = '07'
	while True:
        	ID = ""
        	read_byte1 = PortRF1.read()
        	if read_byte1=="\x02":
                	for Counter in range(12):
                        	read_byte1=PortRF1.read()
                        	ID = ID + str(read_byte1)
			processID(ID,DOOR)
def rfid08():
	global flag
	PortRF1 = serial.Serial('/dev/ttyUSB7',9600)
	DOOR = '08'
	while True:
        	ID = ""
        	read_byte1 = PortRF1.read()
        	if read_byte1=="\x02":
                	for Counter in range(12):
                        	read_byte1=PortRF1.read()
                        	ID = ID + str(read_byte1)
			processID(ID,DOOR)


print("In main block")

t1 = Thread(target=rfid01)
threads = [t1]

t2 = Thread(target=rfid02)
threads += [t2]

t3 = Thread(target=rfid03)
threads += [t3]

t4 = Thread(target=rfid04)
threads += [t4]

t5 = Thread(target=rfid05)
threads += [t5]

t6 = Thread(target=rfid06)
threads += [t6]

t7 = Thread(target=rfid07)
threads += [t7]

t8 = Thread(target=rfid08)
threads += [t8]

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()

print threads

#for tloop in threads:
#    tloop.join()

print("End of main block")
