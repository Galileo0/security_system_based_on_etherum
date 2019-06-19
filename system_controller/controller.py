from flask import Flask, flash, redirect, render_template, request, session, abort
import backend

app = Flask(__name__)
 
@app.route("/")
def index():
    return "Index!"
 
@app.route("/init_vis")
def init_vis():
    return render_template('init_vis_graphic.html')
 
@app.route("/data",methods = ['POST'])
def data():
    name = request.form['_name']
    phone = request.form['_phone_num']
    email = request.form['email']
    car_num = request.form['car_number']  #temp it must scan automatic
    qr_code_duration = request.form['qr_dur']
    backend.block_ch_function(email,qr_code_duration,name,phone,car_num)
    return "Success"
 
if __name__ == "__main__":
    app.run()