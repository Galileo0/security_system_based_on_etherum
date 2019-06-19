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
import serial
# capture | Decode Qrcode
def capture_qr():
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture('http://192.168.1.3:8080/video')
    #cap = cv2.VideoCapture('rtsp://galilio:123123@192.168.1.3')
    token_before = 'Null2'
    #if not cap.isOpened():
       # cap.open(1)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        cv2.imshow('Current',frame)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        #image.tobytes()
        qr_decode = decode(image)
        token = 'NULL'
        if qr_decode:
            #time.sleep(3)
            token = qr_decode[0].data
            token = token.decode('utf-8')
            if token != token_before :
                token_before = token
                print(token)
                auth(token)
                return
                
def _arduino_gate_open():
    port = '/dev/ttyACM0' 
    ard = serial.Serial(port,9600,timeout=5)
    ard.flush()
    ard.write('o'.encode())
            
def auth(token):
    global contract
    global web3
    transact = contract.functions.auth_out(token).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().auth_out(token)
    result = str(result)
    print(result)
    if result == '0':
        auth_worker(token)
        
    elif result == '1':
        transact = contract.functions.check_revoke(token).transact({'from': web3.eth.defalutAccount}) # transaction
        result = contract.call().check_revoke(token)
        result = str(result)
        print (result+' -> revoke')

        if result == '1':
            print ('Access Denied -> Revoked permation')
        else:
            print ('Exit success')
            #access log
            transact = contract.functions.track_in_out(token,'Out Gate1',str(datetime.now())).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().track_in_out(token,'Out Gate1',str(datetime.now()))
            print(str(result))
            #_arduino_gate_open()

    #elif result == '2':
        #scan ID 
        #print ('Plz Provide Your info')
        #complete_data(token)
    else:
        print ('Error')
        


def auth_worker(token):
    global contract
    global web3
    transact = contract.functions.auth_worker(token).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().auth_worker(token)
    result = str(result)
    print(result)

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

    if date_time_com(date_a,days):
        transact = contract.functions.check_revoke(token).transact({'from': web3.eth.defalutAccount}) # transaction
        result = contract.call().check_revoke(token)
        result = str(result)
        print (result+' -> revoke')

        if result == '1':
            print ('Access Denied -> Revoked permation')
        else:
            #open_gate
            print('Exit Success')
            transact = contract.functions.track_in_out_worker(token,'Out Gate1',str(datetime.now())).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().track_in_out_worker(token,'Out Gate1',str(datetime.now()))
            print(str(result))
            #_arduino_gate_open()
        
    else:
        auth_res(token)




def auth_res(_pk):
    global contract
    global web3
    transact = contract.functions.auth_resdent(token).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().auth_resdent(token)
    result = str(result)
    print(result)
    if result == '0':
        print('Exit Denied')
        
    elif result == '1':
        transact = contract.functions.check_revoke(token).transact({'from': web3.eth.defalutAccount}) # transaction
        result = contract.call().check_revoke(token)
        result = str(result)
        print (result+' -> revoke')

        if result == '1':
            print ('Access Denied -> Revoked permation')
        else:
            print('Access')
            #_arduino_gate_open()




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




def complete_data(token):
    name = input('Enter Your Name : ')
    sex =  input("sex : ")
    card_num = input('ID Number : ')
    test_trans = contract.functions.set_I('ahmeed','33').transact({'from': web3.eth.defalutAccount})
    send_data = contract.functions.complete_data(token,name,sex,card_num).transact({'from': web3.eth.defalutAccount})
    result = contract.call().complete_data(token,name,sex,card_num)
    result = str(result)
    print(result)
    if result == '1' :
        print ('Access')
    else:
        print ('Error in update')






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
    gate_account = lines[1]
    gate_account = gate_account.replace('\n','')
    print(gate_account)
    web3.eth.defalutAccount = gate_account
    
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



