#!/usr/bin/python
# Sends data to the Firebase

import socket
import json
import urllib2
import psycopg2
import sys
import time
import os
from firebase import firebase

# variable : unique name (change this)
id_name='/cedt'


#initialization of delay
re_send_interval= 7	# 10 = 7+(3 of sending) seconds	
reconnect_interval= 120	# x*10 seconds
reboot_interval= 720	# x*10seconds=120*6*10seconds
posting_interval= 5	# 10= 5 +( 5 network delay) seconds

#initialization
reconnect=0
reboot=0
#socket_reconnect=0
os.system("ifup wlan0")
firebase = firebase.FirebaseApplication('https://powermonitoring.firebaseio.com/', None)
os.system("echo 1 > /root/power_monitoring/time_flag.txt")
con = None
tf_file = open("/root/power_monitoring/time_flag.txt", "r+")
t_f = tf_file.read(1);
tf_file.close()

def get_time():		
	  time.sleep(2)
	  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	  try:
		  HOST = sys.argv[1]
		  PORT = 5000
		  s.connect((HOST, PORT))
		  a= {'req':'time'}
		  b=json.dumps(a)
  		  s.send(b)
    		  
		  try:
		    data = s.recv(19)
    		    if data:
                        date_time="date --set "+'"'+data+'"'
                        os.system(date_time)
			tf_file = open("/root/power_monitoring/time_flag.txt", "r+")
			tf_file.write("1");
			tf_file.close()
			return '1'
                        s.close()
		  except:
			print "time not received"
    	  except socket.error:
		#global socket_reconnect=socket_reconnect+1
		#if socket_reconnect>10 :
		os.system("ifdown wlan0 && ifup wlan0")
		#	socket_reconnect=0
		print "time : socket error"
		s.close()
		return '0'
	  except :			
		print " time not updated"
		s.close()
		return '0'
while True:
	time.sleep(5)
	try:
	   con = psycopg2.connect("dbname='mydb' user='root'")
	   cur = con.cursor()
	   cur.execute("SELECT COUNT(*) FROM power_data" )
	   count= cur.fetchall()
           count=count[0][0]
	   if count>11:
			try:
				if t_f=='0':
					print "time getting"
					t_f=get_time()			
				cur.execute("SELECT * FROM power_data LIMIT 12" )
				row=cur.fetchall()

				time_data=str(row[0][0])+','+str(row[1][0])+','+str(row[2][0])+','+str(row[3][0])+','+str(row[4][0])+','+str(row[5][0])+','+str(row[6][0])+','+str(row[7][0])+','+str(row[8][0])+','+str(row[9][0])+','+str(row[10][0])+','+str(row[11][0])
				voltage=str(row[0][1])+','+str(row[1][1])+','+str(row[2][1])+','+str(row[3][1])+','+str(row[4][1])+','+str(row[5][1])+','+str(row[6][1])+','+str(row[7][1])+','+str(row[8][1])+','+str(row[9][1])+','+str(row[10][1])+','+str(row[11][1])
				frequency=str(row[0][2])+','+str(row[1][2])+','+str(row[2][2])+','+str(row[3][2])+','+str(row[4][2])+','+str(row[5][2])+','+str(row[6][2])+','+str(row[7][2])+','+str(row[8][2])+','+str(row[9][2])+','+str(row[10][2])+','+str(row[11][2])
				result = firebase.post(id_name,{'t':time_data,'v':voltage,'f':frequency})
	
				print "result"
				print result			
				if result == 'sent':
					print result
					for l in range(0,12):
						cur.execute("DELETE FROM power_data WHERE s=(select s from power_data limit 1);")
					con.commit()
					print "deleted"
					con.close()
					reboot=0
					reconnect=0
					time.sleep(posting_interval)
			except :
				log="echo Exception at"+str(time.time())+' >> /root/power_monitoring/exception.log'			
				os.system(log)
				print "firebase not reached"
				reconnect=reconnect+1
				reboot=reboot+1
				if reconnect>reconnect_interval:
					os.system("ifdown wlan0 && ifup wlan0")
					reconnect=0
				if reboot>reboot_interval:
					os.system("reboot")	
				time.sleep(re_send_interval)
				con.close()	
			
	   else:
			wait=(12-count)*10
			time.sleep(wait)		

		#os.sys("python power_monitoring/on_boot.by")
	except psycopg2.DatabaseError, e:
	   print 'Error %s' % e
	   
	except KeyboardInterrupt:
	   print('Interruption from Keyboard')
	   break
	except socket.error:                                      
	   os.system("ifdown wlan0 && ifup wlan0")
	   get_time() 
		                        
	except:                                    
	   print('General Exception')
