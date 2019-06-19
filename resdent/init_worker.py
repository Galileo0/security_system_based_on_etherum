from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json
import datetime
import time
import qrcode
import send_qr_code
import hashlib
import os

# Bloch chaine Connection 

web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
con_abi = open('../contracts/con_abi','r')
con_abi = con_abi.read()
con_add = open('../contracts/con_add','r')
con_add = con_add.read()
con_byte_code = open('../contracts/con_byte_code','r')
con_byte_code = con_byte_code.read()

#web3.eth.defalutAccount = web3.eth.accounts[4]   ### res Account
con_add = web3.toChecksumAddress(con_add)
bid_abi=json.loads(con_abi)

contract = web3.eth.contract(abi=con_abi,address = con_add)

## Calling Functions

def qr_code(token,_email,qr_duration):
    img = qrcode.make(str(token))
    img.save('qr_code_temp.jpg')
    send_qr_code.send_qr('qr_code_temp.jpg',_email,qr_duration)
    os.remove('qr_code_temp.jpg')

def init_worker(name,duration,email,rf,job,days,pk):
    
    # ----- res account ----- #
    web3.eth.defalutAccount = pk
    #------ End-----#
    # make token + key mangeing -> This is New Version of initating 
    timestamp = time.time()
    token = (str(web3.eth.defalutAccount)+str(duration)+str(timestamp))  # i replaced _email with account of security building 
    token = token.encode('utf-8')
    token = hashlib.sha256(token).hexdigest()

    # contact smart contract 
    tx = contract.functions.init_worker(token,duration,email,days,name,rf,job).transact({'from': web3.eth.defalutAccount})
    rec = web3.eth.getTransactionReceipt(tx)
    print(tx)
    print('---------imp---------')
    print(web3.eth.defalutAccount)
    print(token)
    print('---------End---------')
    qr_code(token,email,duration)