from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from datetime import datetime
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import json
import time
from datetime import date
import os
import sys

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

def auth(token):
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

    if date_time_com(date_a,days):
        #open_gate
        print('Access')
        pass
    else:
        print('Access Denied')

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


## Block Chaine prepare ##
if __name__ == '__main__':
    
        

    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    con_abi = open('../contracts/con_abi','r')
    con_abi = con_abi.read()
    con_add = open('../contracts/con_add','r')
    con_add = con_add.read()
    con_byte_code = open('../contracts/con_byte_code','r')
    con_byte_code = con_byte_code.read()

    web3.eth.defalutAccount = web3.eth.accounts[5]
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
