from flask import Flask, flash, redirect, render_template, request, session, abort
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json
import montering
import os
#import init_worker
#import edit_access
import db_man as db
import sqlite3
import private_key_infrastructure as p_k
import home
import qrcode
import send_qr_code
import add_resdent 
import revoke_controll 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/revoke")
def revoke():
    return render_template('revoke.html')


@app.route("/revoke_post",methods = ['POST'])
def revoke_post():
    email = request.form['email']
    statu = revoke_controll.revoke(email)
    print(statu)
    return redirect("http://127.0.0.1:5000/", code=302)


@app.route("/unrevoke")
def unrevoke():
    return render_template('unrevoke.html')


@app.route("/unrevoke_post",methods = ['POST'])
def unrevoke_post():
    email = request.form['email']
    statu = revoke_controll.unrevoke(email)
    print(statu)
    return redirect("http://127.0.0.1:5000/", code=302)

    
@app.route("/sell_home")
def sell_home():
    return render_template('sell_home.html')


@app.route("/sell_home_post",methods = ['POST'])
def sell_home_post():
    price = request.form['price']
    home_pk = str(p_k.create_pk())
    home.sell_home(home_pk,price)
    return redirect("http://127.0.0.1:5000/", code=302)

@app.route("/cleardb")
def cleardb():
    conn = sqlite3.connect('SBD.db')
    db._clear_db(conn)
    return redirect("http://127.0.0.1:5000/", code=302)

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
    init_worker.init_worker(name,duration,email,rf,job,days)
    return ('Success')

@app.route("/access_controll_edit")
def access_controll_edit():
    return render_template('access_controll_edit.html')


@app.route("/access_controll_edit_post",methods = ['POST'])
def access_controll_edit_post():
    email = request.form['email']
    duration = request.form['Duration']
    days = request.form['days']
    R = edit_access.edit_access(email,duration,days)
    if R == '1':
        return 'Success'
    else:
        return 'No Email Matching'
    


@app.route("/filter")
def init_mon():
    return render_template('init_mon_graphic.html')

@app.route("/create_account")
def create_account():
    return render_template('create_account.html')



def qr_code(token,_email,qr_duration):
    img = qrcode.make(str(token))
    img.save('qr_code_temp.jpg')
    send_qr_code.send_qr('qr_code_temp.jpg',_email,qr_duration)
    os.remove('qr_code_temp.jpg')

@app.route("/create_account_post",methods = ['POST'])
def create_account_db():
    conn = sqlite3.connect('SBD.db')
    user_name = request.form['user_name']
    passw = request.form['pass']
    email = request.form['email']
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    pk = p_k.create_res_pk() # create private key
    print(pk)
    print(pk[0])
    print(pk[1])
    db._insert_data(conn,str(user_name),str(passw),str(pk[1])) # insert to db
    qr_code(pk[0],email,'Resdent Access')
    #account = web3.eth.account.privateKeyToAccount(int(pk))
    #address = account._address
    add_resdent.add_res(email,pk[0],pk[1])
    return redirect("http://127.0.0.1:5000/", code=302)



@app.route("/create_dev_accounts")
def create_dev_accounts():
    p_k.create_dev_pk()
    return redirect("http://127.0.0.1:5000/", code=302)


@app.route("/data",methods = ['POST'])
def data():
    Time = request.form['Time']
    Date = request.form['Date']
    Location = request.form['Location']
    montering.get_visitors()
    montering.get_tracking_logs()
    temp = montering.t_location
    found = []
    found_time = []
    found_location = []
    found_date = []
    found_filter = []
    filter_data = []

    filter_time = []
    filter_date = []
    filter_location = []

    counter = 0
    for x in temp:
        if Location == x:
            found.append(counter)
            found_location.append(counter)
            print('location-found')
        counter+=1


    counter_time = 0
    for x in montering.t_time:
        
        Data = x.split()
        x_time = Data[1]
        x_date = Data[0]
        x_time = x_time[:5]

        if Time == x_time and Date == x_date:
            found_time.append(counter_time)
            print('time found')
        
        if Date == x_date:
            found_date.append(counter_time)
            print('date found')
        counter_time+=1

    
    for x in found:
        #handel strings
        Data = montering.t_time[x]
        Data = Data.split()
        x_time = Data[1]
        x_date = Data[0]
        x_time = x_time[:5]

        if Time == x_time and Date == x_date:
            found_filter.append(x)
    
    # final output

    for x in found_filter:
        data = montering.t_name[x]+' : '+montering.t_phone[x]+' : '+montering.t_rf[x]+' : '+montering.t_location[x]+' : '+montering.t_time[x]+' : '+montering.t_locater_account[x]+' : '+montering.t_res[x]
        filter_data.append(data)
    
    for x in found_time:
        data = montering.t_name[x]+' : '+montering.t_phone[x]+' : '+montering.t_rf[x]+' : '+montering.t_location[x]+' : '+montering.t_time[x]+' : '+montering.t_locater_account[x]+' : '+montering.t_res[x]
        filter_time.append(data)
    
    for x in found_date:
        data = montering.t_name[x]+' : '+montering.t_phone[x]+' : '+montering.t_rf[x]+' : '+montering.t_location[x]+' : '+montering.t_time[x]+' : '+montering.t_locater_account[x]+' : '+montering.t_res[x]
        filter_date.append(data)
    
    for x in found_location:
        data = montering.t_name[x]+' : '+montering.t_phone[x]+' : '+montering.t_rf[x]+' : '+montering.t_location[x]+' : '+montering.t_time[x]+' : '+montering.t_locater_account[x]+' : '+montering.t_res[x]
        filter_location.append(data)
    
    return render_template("data.html", data_filter=filter_data,data_time=filter_time,data_date=filter_date,data_location=filter_location)
    
    #return redirect("http://127.0.0.1:5000/init_vis", code=302)
    
 
if __name__ == "__main__":
    app.run()