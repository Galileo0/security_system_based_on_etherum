import serial
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json
import time
import datetime


# Blochcaine

web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
con_abi = open('../contracts/con_abi','r')
con_abi = con_abi.read()
con_add = open('../contracts/con_add','r')
con_add = con_add.read()
con_byte_code = open('../contracts/con_byte_code','r')
con_byte_code = con_byte_code.read()

# new methods of private keys
file_f = open('../contracts/dev_acc','r')
lines = file_f.readlines()
rf_account = lines[2]
rf_account = rf_account.replace('\n','')
print(rf_account)
web3.eth.defalutAccount = rf_account

con_add = web3.toChecksumAddress(con_add)
bid_abi=json.loads(con_abi)

contract = web3.eth.contract(abi=con_abi,address = con_add)

RF_location = 'street 33'
#-----------------------------

# serail communication 
port = '/dev/ttyUSB1' #arduino serial port
ard = serial.Serial(port,9600,timeout=5) # connect with paud rate

while True:
    msg = ard.read(ard.inWaiting()) # read everything in the input buffer
    detected_rf = ''
    if msg != b'':
        detected_rf = detected_rf + msg.decode("utf-8")
        if len(detected_rf)==8 :
            print(detected_rf)
            # ------ block-chaine -------
            transact = contract.functions.track(detected_rf,RF_location,str(datetime.datetime.now())).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().track(detected_rf,RF_location,str(datetime.datetime.now()))
            result = str(result)
            print(result + ' result from contract ')
            #-----------------------
            # ------ block-chaine -------
            transact = contract.functions.track_worker(detected_rf,RF_location,str(datetime.datetime.now())).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().track_worker(detected_rf,RF_location,str(datetime.datetime.now()))
            result = str(result)
            print(result + ' result from contract ')
            #-----------------------
            # ------ end-block ----------
    else:
        if detected_rf != '':
            print (detected_rf)


