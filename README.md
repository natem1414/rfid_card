# rfid_card

#Place in /usr/local/bin/rfid/rfidreader.py
#card01.txt
#card02.txt
#card03.txt
#card04.txt
#card05.txt
#card06.txt
#card07.txt
#card08.txt

#Place in /etc/systemd/system/
#rfidreader.service

#Not Needed:
#weekdaytest.py

#Run command:

sudo systemctl daemon-reload
sudo systemctl start myscript.service
sudo systemctl enable myscript.service
