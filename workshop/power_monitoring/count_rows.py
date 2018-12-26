import psycopg2

try:
    con = psycopg2.connect("dbname='mydb' user='root'")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM power_data " )
    count= cur.fetchall()
    print count[0][0]
except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)

