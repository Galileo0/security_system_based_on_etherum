from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json
import hashlib
import time
import qrcode
import send_qr_code
import os

def block_ch_function(_email,qr_duration,_name,_phone_num,car_num,pk):

    web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
    con_abi = open('../contracts/con_abi','r')
    con_abi = con_abi.read()
    con_add = open('../contracts/con_add','r')
    con_add = con_add.read()
    con_byte_code = open('../contracts/con_byte_code','r')
    con_byte_code = con_byte_code.read()

    

    
    web3.eth.defalutAccount = pk  
    con_add = web3.toChecksumAddress(con_add)
    bid_abi=json.loads(con_abi)

    contract = web3.eth.contract(abi=con_abi,address = con_add)
    
    # make token
    timestamp = time.time()
    token = (_email+str(qr_duration)+str(timestamp))
    token = token.encode('utf-8')
    token = hashlib.sha256(token).hexdigest()

    # contact smart contract 

    tx = contract.functions.init_visiting(token,int(qr_duration),_email,_phone_num,_name,car_num).transact({'from': web3.eth.defalutAccount})
    rec = web3.eth.getTransactionReceipt(tx)
    print(tx)
    qr_code(token,_email,qr_duration)




def init_vis(_email,qr_duration,_name,_phone_num,car_num,pk): 
    # make token
    timestamp = time.time()
    token = (_email+str(qr_duration)+str(timestamp))
    token = token.encode('utf-8')
    token = hashlib.sha256(token).hexdigest()
    # contact smart contract 
    tx = contract.functions.init_visiting(token,int(qr_duration),_email,_phone_num,_name,car_num).transact({'from': web3.eth.defalutAccount})
    rec = web3.eth.getTransactionReceipt(tx)
    print(tx)
    qr_code(token,_email,qr_duration)


def qr_code(token,_email,qr_duration):
    img = qrcode.make(str(token))
    img.save('qr_code_temp.jpg')
    send_qr_code.send_qr('qr_code_temp.jpg',_email,qr_duration)
    os.remove('qr_code_temp.jpg')

