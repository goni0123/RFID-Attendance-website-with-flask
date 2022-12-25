import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
import mariadb
import datetime
reader = SimpleMFRC522()
while True:
    conn = mariadb.connect(user='admin', password='password',db='Attended', host='localhost')
    c = conn.cursor()
    d1 = datetime.datetime.today().strftime('%Y%m%d')
    c.execute("INSERT INTO attended(E_name,E_date)SELECT Event_name, Event_date FROM Event WHERE Event_date = {}".format(f'{d1}'))
    conn.commit()
    c.close()
    rfid, text = reader.read()
    while rfid < 0:
        rfid, text = reader.read()
        c.execute("INSERT INTO attended(A_name,rfid_uid)SELECT name,rfid_uid FROM users WHERE rfid_uid = {}".format(rfid))
        conn.commit()
        
        c.execute("SELECT A_in FROM attended where rfid_uid = '{}'".format(rfid))
        conn.commit()
        io = c.fetchall()
        c.close()
        if io == 0:
            t1 = datetime.datetime.today().strftime('%H:%M')
            c.execute("INSERT INTO attended(A_in) value ({})".format(t1))
            conn.commit()
            conn.close()
            c.close()
        else:
            t1 = datetime.datetime.today().strftime('%H:%M')
            c.execute("INSERT INTO attended(A_out) value ({})".format(t1))
            conn.commit()
            conn.close()
            c.close()
