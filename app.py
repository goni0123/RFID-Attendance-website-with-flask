import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from mfrc522 import SimpleMFRC522
import mariadb
reader = SimpleMFRC522()

app =Flask(__name__)

@app.route('/')
@app.route('/Attendance')
def Attendance():
    return render_template(Attendance.html)


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
    c.execute("INSERT INTO users (id,rfid_uid,name) VALUES ({},'{}',{})".format(int(id), name, int(rfid)))
    conn.commit()
    conn.close()
    c.close()
  return render_template('Adduser.html') 

@app.route('/Addevent', methods=['GET','POST'])
def Addevent():
  if request.method=='POST':
    Event_id=request.form.get('Event_id')
    Event_name=request.form.get('Event_name')
    Data_start=request.form.get('Data_start')
    Data_finish=request.form.get('Data_finish')
    conn=mariadb.connect(user='admin', password='password',db='Attended', host='localhost')
    c=conn.cursor()
    c.execute("INSERT INTO Event(Event_id,Event_name,Data_start,Data_finish) VALUES ({},'{}','{}','{}')".format(int(Event_id), Event_name, Data_start, Data_finish))
    conn.commit()
    conn.close()
    c.close()
  return render_template('Addevent.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
