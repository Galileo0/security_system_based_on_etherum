from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json
import hashlib
import time
import os
import re


#Global_Arrays

#----- visiting ------#
counter_vis = 0
name = []
phone = []
rf = []
qr_code_ex = []
token = []
resdent_account = []
email = []

#------ end -------#

#------- Track ------#
counter_track = 0     # number of Logs
t_name = []           
t_phone = []
t_rf = []
t_location = []
t_time = []
t_locater_account = []
t_res = []
#------ end -------#
Visiting_log = []
Workers_log = []
Tracking_log = []
#------------


# Bloch chaine Connection 

web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
con_abi = open('../contracts/con_abi','r')
con_abi = con_abi.read()
con_add = open('../contracts/con_add','r')
con_add = con_add.read()
con_byte_code = open('../contracts/con_byte_code','r')
con_byte_code = con_byte_code.read()

web3.eth.defalutAccount = web3.eth.accounts[9]   ### Security Building Account
con_add = web3.toChecksumAddress(con_add)
bid_abi=json.loads(con_abi)

contract = web3.eth.contract(abi=con_abi,address = con_add)

## Calling Functions

def get_visitors():
    # get count first 
    transact = contract.functions.get_visitor_count().transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().get_visitor_count()
    visitors_count = int(result)
    
    #loop to get data from blockchaine

    for x in range(1,(visitors_count+1)):
        transact = contract.functions.get_visitor(x).transact({'from': web3.eth.defalutAccount}) # transaction
        data = contract.call().get_visitor(x)
        data = str(data)
        Visiting_log.append(data)
        print(data)

def get_worker():
         # get count first 
    transact = contract.functions.get_workers_count().transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().get_workers_count()
    workers_count = int(result)
    
    #loop to get data from blockchaine

    for x in range(1,(workers_count+1)):
        transact = contract.functions.get_worker(x).transact({'from': web3.eth.defalutAccount}) # transaction
        data = contract.call().get_worker(x)
        data = str(data)
        Workers_log.append(data)
        print(data)



def get_tracking_logs():
    # get count first 
    transact = contract.functions.get_track_logs_count().transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().get_track_logs_count()
    logs_count = int(result)
    
    #loop to get data from blockchaine

    for x in range(1,(logs_count+1)):
        transact = contract.functions.get_track(x).transact({'from': web3.eth.defalutAccount}) # transaction
        data = contract.call().get_track(x)
        data = str(data)
        Tracking_log.append(data)
        handel_string_tracking(data)
        print(data)



def handel_string_tracking(string):
    global counter_track;global t_name;global t_phone;global t_rf;global t_location;global t_time;global t_locater_account;global t_res;
    res = re.findall(r"'([A-Za-z\s]*)'(,|\s)*'([0-9]*)'(,|\s)*'([0-9A-F]*)'(,|\s)*'([A-Za-z0-9\s]*)'(,|\s)*'([0-9\-\s\:\.]*)'(,|\s)*'([0-9a-zA-Z]*)'(,|\s)*'([0-9a-zA-Z]*)'",string)
    print('w')
    for (name,t,num,t,code,t,add,t,time,t,sh,t,sb) in res:
        t_name.append(name)
        t_phone.append(num)
        t_rf.append(code)
        t_location.append(add)
        t_time.append(time)
        t_locater_account.append(sh)
        t_res.append(sb)
        counter_track+=1



# Searching 


'''def handel_string_tracking(string):
    global counter_track
    res = re.findall(r"'([A-Za-z\s]*)'(,|\s)*'([0-9]*)'(,|\s)*'([0-9A-F]*)'(,|\s)*'([A-Za-z0-9\s]*)'(,|\s)*'([0-9\-\s\:\.]*)'(,|\s)*'([0-9a-zA-Z]*)'",string)
    for (name,t,num,t,code,t,add,t,time,t,sh) in res:
        t_name.append(name)
        t_phone.append(num)
        t_rf.append(code)
        t_location.append(add)
        t_time.append(time)
        t_locater_account.append(sh)
        counter_track+=1

'''
#get_visitors()
#get_tracking_logs()