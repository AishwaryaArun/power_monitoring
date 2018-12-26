#!/usr/bin/python
# To copy all data in the database to a csv file in /root/power_monitoring

import psycopg2
import sys

con = None

try:
    con = psycopg2.connect("dbname='mydb' user='root'")
    cur = con.cursor()
    cur.execute("\COPY (SELECT * from power_data) TO '/root/power_monitoring/power_data.csv' WITH csv;")
    con.commit()
    con.close()
except:
        print "Exception"
