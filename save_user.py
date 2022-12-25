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
d1 = datetime.datetime.today().strftime('%Y%m%d')

c = conn.cursor()
c.execute("INSERT INTO attended(E_name,E_date,A_name,rfid_uid) SELECT Event.Event_name, Event.Event_date, users.name,users.rfid_uid FROM Event INNER JOIN users WHERE users.rfid_uid = {} AND Event.Event_date= {}".format(rfid,d1))

c = conn.cursor()
c.execute("SELECT A_in FROM attended where rfid_uid = '{}'".format(rfid))
io = c.fetchall()

c.close()
if io == None:
  c = conn.cursor()
  t1 = datetime.datetime.today().strftime('%Y%m%d %H:%M')

  c.execute("INSERT INTO attended(A_in) VALUES ('{}') SELECT A_in from attended where rfid_uid = {}".format(t1,rfid))
  conn.commit()
  conn.close()
  c.close()
elif io!=None:
  c = conn.cursor()
  t1 = datetime.datetime.today().strftime('%Y%m%d %H:%M')
  c.execute("INSERT INTO attended(A_out) values ('{}') SELECT (A_out) from attended  where rfid_uid= {}".format(t1, rfid))
  conn.commit()
  conn.close()
  c.close()
