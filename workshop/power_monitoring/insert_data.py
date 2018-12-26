#!/usr/bin/python
#Inserts data into the table 'power_data'

import psycopg2
import sys
import time
con = None

try:
    con = psycopg2.connect("dbname='mydb' user='root'")
    cur = con.cursor()
    
    data_entry="INSERT INTO power_data VALUES("+str(time.time())+','+(sys.argv[1])+','+(sys.argv[2])+')'
    cur.execute(data_entry)
    con.commit()

except psycopg2.DatabaseError, e:

    if con:
        con.rollback()
    print 'Error %s' % e
    sys.exit(1)
finally:
    if con:
        con.close()


