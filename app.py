import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
import mariadb
from flask_table import Table, Col
import datetime

reader = SimpleMFRC522()

app =Flask(__name__)


def Attend():
  rfid, text = reader.read()
  while rfid < 0:
    rfid, text = reader.read()
  conn = mariadb.connect(user='admin', password='password',db='Attended', host='localhost')
  c = conn.cursor(buffered=True)
  query = ("SELECT * FROM attended where rfid_uid = '{}'".format(rfid))
  c.execute(query)
  print(c.rowcount)
  if c.rowcount == 0:
    d1 = datetime.datetime.today().strftime('%Y%m%d')
    t1 = datetime.datetime.today().strftime('%H:%M')
    c = conn.cursor()
    c.execute("INSERT INTO attended(E_name,E_date,A_name,rfid_uid) SELECT Event.Event_name, Event.Event_date, users.name,users.rfid_uid FROM Event INNER JOIN users WHERE users.rfid_uid = {} AND Event.Event_date= {}".format(rfid, d1))
    c.execute("update attended set A_in =('{}') where rfid_uid = ('{}')".format(t1, rfid))
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

@app.route('/')
def attended():
  while True:
      Attend()
  
@app.route('/Attendance', methods=['GET', 'POST'])
def Attendance():
  if request.method == "POST":
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM attended")

  # Fetch the results of the query
    users = cur.fetchall()

  # Render the results in a template
    return render_template("Attendance.html", users=users)
  else:
    return render_template("Attendance.html")


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
    c = conn.cursor(buffered=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

  # Fetch the results of the query
    users = cur.fetchall()

  # Render the results in a template
    return render_template("Users.html", users=users)
  else:
    return render_template("Users.html")



@app.route('/Events', methods=['GET', 'POST'])
def Events():
  if request.method == "POST":
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Event")

  # Fetch the results of the query
    users = cur.fetchall()

  # Render the results in a template
    return render_template("Events.html", users=users)
  else:
    return render_template("Events.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
