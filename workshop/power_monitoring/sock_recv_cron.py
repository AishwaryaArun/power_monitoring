# Connects to the network and gets time from the access point and runs arduino sketch on boot
import socket
import sys
import json
import time
import os

tf_file = open("/root/power_monitoring/time_flag.txt", "r+")
tf_file.write("0");
tf_file.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(2)	
try:
		  HOST = sys.argv[1]
		  PORT = 5000
		  s.connect((HOST, PORT))
		  a={'req':'time'}
		  b=json.dumps(a)
  		  s.send(b)
		  print b
		  try:
            		data = s.recv(19)
            		if data:
                		
                                date_time="date --set "+'"'+data+'"'
                                os.system(date_time)
                                tf_file = open("/root/power_monitoring/time_flag.txt", "r+")
				tf_file.write("1");
				tf_file.close() 
	               	        s.close()
            	  
        	  except:
			print "no ack"			
			s.close()
except KeyboardInterrupt:
		  print('Interruption from Keyboard')
		  s.close()
except socket.error:                                      
		  print('Socket Error')
		  s.close()                             
except:                                    
		  print('General Exception')
		  s.close()
        

