import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
import mariadb
from flask_table import Table, Col
import datetime

reader = SimpleMFRC522()

app =Flask(__name__)


def Attend():
  while True:
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor()
    d1 = datetime.datetime.today().strftime('%Y%m%d')
    c.execute("INSERT INTO attended(E_name,E_date)SELECT Event_name, Event_date FROM Event WHERE Event_date = {}".format(f'{d1}'))
    conn.commit()
    c.close()
    rfid, text = reader.read()
    while rfid < 0:
        rfid, text = reader.read()
        c.execute(
            "INSERT INTO attended(A_name,rfid_uid)SELECT name,rfid_uid FROM users WHERE rfid_uid = {}".format(rfid))
        conn.commit()
        c.close()
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

@app.route('/')
@app.route('/Attendance', methods=['GET', 'POST'])
def Attendance():
  rfid, text = reader.read()
  while rfid < 0:
    rfid, text = reader.read()
    Attend()

  return render_template('Attendance.html')


@app.route('/Adduser', methods=['GET','POST'] )
def Adduser():
  if request.method=='POST':
    rfid, text = reader.read()
    while rfid < 0:
      rfid, text = reader.read()
    id=request.form.get('id')
    name=request.form.get('name')
    conn = mariadb.connect(user='admin', password='password',db='Attended', host='localhost')
    c = conn.cursor()
    c.execute("INSERT INTO users (id,name,rfid_uid) VALUES ({},'{}',{})".format(int(id), name, int(rfid)))
    conn.commit()
    conn.close()
    c.close()
  return render_template('Adduser.html') 

@app.route('/Addevent', methods=['GET','POST'])
def Addevent():
  if request.method=='POST':
    Event_name=request.form.get('Event_name')
    Data_start=request.form.get('Data_start')
    conn=mariadb.connect(user='admin', password='password',db='Attended', host='localhost')
    c=conn.cursor()
    data = Data_start
    c.execute("INSERT INTO Event(Event_name,Event_date) VALUES ('{}','{}')".format(Event_name, data))
    conn.commit()
    conn.close()
    c.close()
  return render_template('Addevent.html')


@app.route('/Users', methods=['GET', 'POST'])
def Users():
  if request.method == "POST":
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor()
    c.execute("SELECT * FROM users ")
    output = c.fetchone()
    c.close
    return render_template("Users.html", data=output)
  else:
    return render_template("Users.html")


@app.route('/Events', methods=['GET', 'POST'])
def Events():
  if request.method == "POST":
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor()
    c.execute("SELECT * FROM Event ")
    output = c.fetchone()
    c.close
    return render_template("Events.html", data=output)
  else:
    return render_template("Events.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
