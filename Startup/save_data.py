import MySQLdb as mdb
import sys

con = None
con = mdb.connect('localhost', 'python_robot', '', 'JobData')
with con:
	cur = con.cursor()
	cur.execute("INSERT INTO Company (Name,Industry,Property,Scale) VALUES ('CName1','Industry1','Property!','Scale!!')")
	cur.execute("SELECT * FROM Company")
	rows = cur.fetchall()
for row in rows:
	print row
