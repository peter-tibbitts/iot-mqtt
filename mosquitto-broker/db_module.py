from datetime import date, datetime, timedelta
import mysql.connector

def insertTempRecord(temp,ts):
	cnx = mysql.connector.connect(user='root', password='root', database='iot')
	cursor = cnx.cursor()

	add_record = ("INSERT INTO temperature "
               "(datetime, temp) "
               "VALUES (%s, %s)")

	record_data = (ts, temp)

	# Insert new record
	cursor.execute(add_record, record_data)
	emp_no = cursor.lastrowid

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()
