# rfid_card

#Equipment Needed:  
Raspberry pi  
Door Lock with GPI (can also send a TCP command, for example to HomeSeer)
RS232 to USB  
RFID Cards:
https://www.ebay.com/itm/New-Contactless-125KHz-RFID-Proximity-Smart-ID-Card-1-8mm-Thinkness-EM4100-4102/291435244981?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649

Card reader:  
https://www.ebay.com/itm/Daul-Led-Epoxy-Fulled-125KHz-RS232-COM-port-EM4100-4102-RFID-card-pigtail-READER/254018797313?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649



#Place in /usr/local/bin/rfid/rfidreader.py  
card01.txt  
card02.txt  
card03.txt  
card04.txt  
card05.txt  
card06.txt  
card07.txt  
card08.txt  

#Place in /etc/systemd/system/  
rfidreader.service

#Not Needed:  
weekdaytest.py

#Run command:  
sudo systemctl daemon-reload  
sudo systemctl start myscript.service  
sudo systemctl enable myscript.service
