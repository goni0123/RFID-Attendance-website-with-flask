import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
import mariadb
import datetime
reader = SimpleMFRC522()

rfid, text = reader.read()
while rfid < 0:
  rfid, text = reader.read()
conn = mariadb.connect(user='admin', password='password', db='Attended', host='localhost')

c = conn.cursor(buffered=True)
query=("SELECT * FROM attended where rfid_uid = '{}'".format(rfid))
c.execute(query)
print(c.rowcount)
if c.rowcount == 0:
  d1 = datetime.datetime.today().strftime('%Y%m%d')
  t1 = datetime.datetime.today().strftime('%H:%M')
  c = conn.cursor()
  c.execute("INSERT INTO attended(E_name,E_date,A_name,rfid_uid) SELECT Event.Event_name, Event.Event_date, users.name,users.rfid_uid FROM Event INNER JOIN users WHERE users.rfid_uid = {} AND Event.Event_date= {}".format(rfid, d1))
  c.execute("update attended set A_in =('{}') where rfid_uid = ('{}')".format(t1,rfid))
  conn.commit()
  conn.close()
  c.close()
else:
  t1 = datetime.datetime.today().strftime('%H:%M')
  c = conn.cursor()
  c.execute("update attended set A_out =('{}') where rfid_uid = ('{}')".format(t1, rfid))
  conn.commit()
  conn.close()
  c.close()
