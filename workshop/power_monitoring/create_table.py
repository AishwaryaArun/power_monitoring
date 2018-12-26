#!/usr/bin/python
# Creates a table 'power_data' in the database 'mydb'
# variable : table name

import psycopg2
import sys

con = None

try:
    con = psycopg2.connect("dbname='mydb' user='root'")
    cur = con.cursor()
    cur.execute("CREATE TABLE power_data(s INTEGER PRIMARY KEY, voltage INT, frequency REAL)")
    con.commit()
except psycopg2.DatabaseError, e:

    if con:
        con.rollback()
    print 'Error %s' % e
    sys.exit(1)
finally:
    if con:
        con.close()

