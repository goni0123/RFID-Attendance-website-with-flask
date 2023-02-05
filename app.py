import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
import mariadb
from flask_table import Table, Col
import datetime
import time

reader = SimpleMFRC522()

app =Flask(__name__)


def Attend():
  reader = SimpleMFRC522()
  while True:
    reader = SimpleMFRC522()
    rfid, text = reader.read()
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    d1 = datetime.datetime.today().strftime('%Y%m%d')
    t1 = datetime.datetime.today().strftime('%H:%M:%S')
    c = conn.cursor()

    c.execute(
        "SELECT * from attended WHERE E_date = {} AND rfid_uid = {}".format(d1, rfid))
    data = c.fetchall()

    if not data:
      c.execute("INSERT INTO attended(E_name,E_date,A_name,rfid_uid,A_in) SELECT Event.Event_name, Event.Event_date, users.name,users.rfid_uid,'{}' FROM Event INNER JOIN users WHERE users.rfid_uid = {} AND Event.Event_date= {}".format(t1, rfid, d1))
      check = "Checked in"
    else:
      c.execute("UPDATE attended SET A_out = '{}' WHERE E_date = {} AND rfid_uid = {}".format(t1, d1, rfid))
      check = "Checked out"

    conn.commit()
    conn.close()
    c.close()
def Attend1():
  reader = SimpleMFRC522()
  while True:
    reader = SimpleMFRC522()
    rfid, text = reader.read()
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    d1 = datetime.datetime.today().strftime('%Y%m%d')
    t1 = datetime.datetime.today().strftime('%H:%M:%S')
    c = conn.cursor()
    c.execute("INSERT INTO attended(E_name,E_date,A_name,rfid_uid,A_in) SELECT Event.Event_name, Event.Event_date, users.name,users.rfid_uid,'{}' FROM Event INNER JOIN users WHERE users.rfid_uid = {} AND Event.Event_date= {}".format(t1, rfid, d1))
    check ="Your are attended"
    conn.commit()
    conn.close()
    c.close()


def Attend2():
  reader = SimpleMFRC522()
  while True:
    reader = SimpleMFRC522()
    rfid, text = reader.read()
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    d1 = datetime.datetime.today().strftime('%Y%m%d')
    t1 = datetime.datetime.today().strftime('%H:%M:%S')
    c = conn.cursor()
    c.execute("INSERT INTO attended(E_name,E_date,A_name,rfid_uid,A_in) SELECT Event.Event_name, Event.Event_date, users.name,users.rfid_uid,'{}' FROM Event INNER JOIN users WHERE users.rfid_uid = {} AND Event.Event_date= {}".format(t1, rfid, d1))
    if c.rowcount == 1: 
      time.sleep(3) 
    check = "Your are attended"
    conn.commit()
    conn.close()
    c.close()


@app.route('/', methods=['GET', 'POST'])
@app.route('/TakeAttendance', methods=['GET', 'POST'])
def TakeAttendance():
  if request.method =="POST":
    time.sleep(1)
    Attend()
    
    return render_template("TakeAttendance.html")
  else :
    return render_template("TakeAttendance.html")
    
  
    

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

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
  if request.method == "POST":
    name = request.form.get('user')
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE name='{}'".format(name))
    conn.commit()


  cur.execute("SELECT * FROM users")

# Fetch the results of the query
  users = cur.fetchall()

# Render the results in a template
  return render_template("Users.html", users=users)



@app.route('/Report', methods=['GET', 'POST'])
def Report():
  if request.method == "POST":
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    name = request.form.get('name')
    Data_start = request.form.get('Data_start')
    c = conn.cursor(buffered=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM attended  WHERE E_date between '{}' and '{}' ".format(Data_start, name))

  # Fetch the results of the query
    users = cur.fetchall()

  # Render the results in a template
    return render_template("Report.html", users=users)
  else:
    return render_template("Report.html")



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
@app.route('/delete_event', methods=['GET','POST'])
def delete_event():
  if request.method == "POST":
    Event_name=request.form.get('event')
    conn = mariadb.connect(user='admin', password='password',
                           db='Attended', host='localhost')
    c = conn.cursor(buffered=True)
    cur = conn.cursor()
    cur.execute("DELETE FROM Event WHERE Event_name='{}'".format(Event_name))
    conn.commit()
  
    cur.execute("SELECT * FROM Event")

  # Fetch the results of the query
    users = cur.fetchall()

  # Render the results in a template
    return render_template("Events.html", users=users)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
