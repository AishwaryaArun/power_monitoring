#!/usr/bin/python
# this code inserts 7 values to the code

import psycopg2
import sys

con = None

try:
    con = psycopg2.connect("dbname='mydb' user='root'")
    cur = con.cursor()
    cur.execute("DELETE from power_data *")
    con.commit()
    con.close()
except:
        print "Exception"
