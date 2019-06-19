from flask import Flask, flash, redirect, render_template, request, session, abort
import backend
import edit_access
import sqlite3
import init_worker
import buy_home as bh
app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('index.html')
    

@app.route("/init_vis")
def init_vis():
    return render_template('init_vis_graphic.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/dologin",methods = ['POST'])
def dologin():
    user_name = request.form['user_name']
    passw = request.form['pass']

    #--- DB ---#
    conn = sqlite3.connect('../SecurityB/SBD.db')
    for x in conn.execute('SELECT * FROM users'):
        if x[0] == user_name and x[1] == passw:
            session['pk']=x[2]  # save private key in session
            return redirect("http://127.0.0.1:5001/", code=302)
    #---- End --- #
    return redirect("http://127.0.0.1:5001/login", code=302)
 
@app.route("/data",methods = ['POST'])
def data():
    name = request.form['_name']
    phone = request.form['_phone_num']
    email = request.form['email']
    car_num = request.form['rf_number']  #temp it must scan automatic
    qr_code_duration = request.form['qr_dur']
    pk = session['pk']
    backend.block_ch_function(email,qr_code_duration,name,phone,car_num,pk)
    return redirect("http://127.0.0.1:5001/init_vis", code=302)
    


@app.route("/access_controll")
def access_controll():
    return render_template('access_controll.html')

@app.route("/access_controll_init",methods = ['POST'])
def access_controll_init():
    name = request.form['_name']
    duration = request.form['qr_dur']
    email = request.form['email']
    rf = request.form['rf_number']
    job = request.form['job']
    days = request.form['days']
    pk = session['pk']
    init_worker.init_worker(name,duration,email,rf,job,days,pk)
    return redirect("http://127.0.0.1:5001/access_controll", code=302)

@app.route("/access_controll_edit")
def access_controll_edit():
    return render_template('access_controll_edit.html')


@app.route("/access_controll_edit_post",methods = ['POST'])
def access_controll_edit_post():
    email = request.form['email']
    duration = request.form['Duration']
    days = request.form['days']
    pk = session['pk']
    R = edit_access.edit_access(email,duration,days,pk)
    if R == '1':
        return 'Success'
    else:
        return 'No Email Matching'

@app.route("/buy_home")
def buy_home():
    pk = session['pk']
    data = bh.get_home(pk) # bh -> buy home module
    return render_template('buy_home.html',data = data)

 
if __name__ == "__main__":
    app.secret_key = '$ilent%%cyberG0101'
    app.run(host='127.0.0.1', port=5001)
    