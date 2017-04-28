
#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import os
import time
import datetime
import glob
import MySQLdb
from time import strftime

continue_reading = True
id_temp=0

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "RFID Login System"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        
        #print "Card read UID: "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])
	id=str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])
	
	#Avoid Repeat read UID Card
	if(id!=id_temp):
		print id
		id_temp=id	


    		#Connect Database
		db = MySQLdb.connect(host="localhost", user="root",passwd="123", db="Member")
		cur = db.cursor()

		# Search Member in Database
   		if(cur.execute("SELECT *FROM `memberlog` WHERE ID=%s;",[id])):
	        	
			#If a card is member that insert database	
			try:
        			db.commit()
  				print "welcome!"
				for row in cur.fetchall():
					print row[0]
					cur.execute("""INSERT INTO Login (datetime,Name) VALUES (%s,%s)""",(datetimeWrite,row[0]))
 					db.commit()
			
    			except:
        			# Rollback in case there is any error
        			db.rollback()
        			print "Failed writing to database"
		else:
	     		db.commit()
	     		print "fail!"	
	

		cur.close()
    		db.close()

