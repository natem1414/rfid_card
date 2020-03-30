# rfid_card

#Equipment Needed:  
Raspberry pi  
Door Lock with GPI  
RS232 to USB  
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
