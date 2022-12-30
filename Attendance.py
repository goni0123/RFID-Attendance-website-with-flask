import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
import mariadb
import datetime
reader = SimpleMFRC522()
while True:
    rfid, text = reader.read()
    conn = mariadb.connect(user='admin', password='password',
                         db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    d1 = datetime.datetime.today().strftime('%Y%m%d')
    t1 = datetime.datetime.today().strftime('%H:%M')
    c = conn.cursor()
    c.execute("INSERT INTO attended(E_name,E_date,A_name,rfid_uid,A_in) SELECT Event.Event_name, Event.Event_date, users.name,users.rfid_uid,{} FROM Event INNER JOIN users WHERE users.rfid_uid = {} AND Event.Event_date= {}".format(rfid, d1,t1))
    conn.commit()
    conn.close()
    c.close()
    
