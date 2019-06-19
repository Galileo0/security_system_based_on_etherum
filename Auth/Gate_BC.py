from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import json
import time
#import datetime
from datetime import datetime
from datetime import date
import os
import sys
# GPIO
import RPi.GPIO as GPIO              #raspri import
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization
# --- GPIO-End-----


import private_key_infrastructure as pk

# capture | Decode Qrcode
def capture_qr():
    cap = cv2.VideoCapture(0)
    token_before = 'Null2'
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        cv2.imshow('Current',frame)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        qr_decode = decode(image)
        token = 'NULL'
        if qr_decode:
            token = qr_decode[0].data
            token = token.decode('utf-8')
            if token != token_before :
                token_before = token
                print(token)
                auth(token)
                return
                
            
            
def auth(token):
    global contract
    global web3
    transact = contract.functions.auth(token).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().auth(token)
    result = str(result)
    print(result)
    if result == '0':
        auth_worker(token)
    elif result == '1':
        #check revoke permation
        transact = contract.functions.check_revoke(token).transact({'from': web3.eth.defalutAccount}) # transaction
        result = contract.call().check_revoke(token)
        result = str(result)
        if result == '1':
            print ('Access Denied -> Revoked permation')
        else:
            print ('Access')
            #access log
            transact = contract.functions.track_in_out(token,'Access Gate1',str(datetime.now())).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().track_in_out(token,'Access Gate1',str(datetime.now()))
            print(str(result))
            SetAngle(180)
            time.sleep(2)
            SetAngle(0)
    else:
        print('Error')


def auth_worker(token):
    global contract
    global web3
    transact = contract.functions.auth_worker(token).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().auth_worker(token)
    result = str(result)
    print(result)
    #handeling string 
    result = result.replace('[','')
    result = result.replace(']','')
    result = result.replace("'","")
    result = result.replace(' ','')
    result = result.split(',')
    # final 
    date_a = result[0]
    days = result[1]
    print(date_a)
    print(days)
    if date_a != 'NULL':
        if date_time_com(date_a,days):
            # check revoke
            transact = contract.functions.check_revoke(token).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().check_revoke(token)
            result = str(result)

            if result == '1':
                print ('Access Denied -> Revoked permation')
            else:
            #open_gate
                print('Access')
                transact = contract.functions.track_in_out_worker(token,'Access Gate1',str(datetime.now())).transact({'from': web3.eth.defalutAccount}) # transaction
                result = contract.call().track_in_out_worker(token,'Access Gate1',str(datetime.now()))
                print(str(result))
                SetAngle(180)
                time.sleep(2)
                SetAngle(0)

        else:
            print('Access Denied')
    else:
        auth_res(token)


def auth_res(token):
    global contract
    global web3
    transact = contract.functions.auth_resdent(token).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().auth_resdent(token)
    result = str(result)
    print(result)
    if result == '0':
        print('Access Denied')
    elif result == '1':
        #check revoke permation
        transact = contract.functions.check_revoke(token).transact({'from': web3.eth.defalutAccount}) # transaction
        result = contract.call().check_revoke(token)
        result = str(result)
        print (result+' -> revoke')

        if result == '1':
            print ('Access Denied -> Revoked permation')
        else:
            print('Access')
            SetAngle(180)
            time.sleep(2)
            SetAngle(0)


def date_time_com(Date_time,days):
    current_date = datetime.now()
    current_week_name = date.today().weekday()
    temp_year = Date_time[6:10]  # index of string 
    temp_month = Date_time[3:5]
    temp_day = Date_time[0:2]

    temp_date = datetime(int(temp_year), int(temp_month), int(temp_day))

    if temp_date > current_date and str(current_week_name) in days:
        return 1
    else:
        return 0





# Servo-motor controll

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(17, True)
	p.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(17, False)
	p.ChangeDutyCycle(0)
#--------------------


## Block Chaine prepare ##
if __name__ == '__main__':
    
        

    web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
    con_abi = open('../contracts/con_abi','r')
    con_abi = con_abi.read()
    con_add = open('../contracts/con_add','r')
    con_add = con_add.read()
    con_byte_code = open('../contracts/con_byte_code','r')
    con_byte_code = con_byte_code.read()

    # ----- Gate account ----- #
    # new methods of private keys
    file_f = open('../contracts/dev_acc','r')
    lines = file_f.readlines()
    gate_account = lines[0]
    gate_account = gate_account.replace('\n','')
    print(gate_account)
    web3.eth.defalutAccount = gate_account
    #------- End -------- #
    #web3.eth.defalutAccount = web3.eth.accounts[5]
    con_add = web3.toChecksumAddress(con_add)
    bid_abi=json.loads(con_abi)

    contract = web3.eth.contract(abi=con_abi,address = con_add)

    #tx_hash = contract.constructor().transact()


    #test_trans = contract.functions.set_I('ahmeed','33').transact({'from': web3.eth.defalutAccount})
    #tx = contract.functions.save('aa','aa','aa','aa','aa','aa').transact({'from': web3.eth.defalutAccount})


    #print(test_trans)



    while True:
        capture_qr()
    #os.execv(__file__, sys.argv)  # Run a new iteration of the current script, providing any command line args from the current iteration.



