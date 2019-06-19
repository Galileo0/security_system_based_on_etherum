import random
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json

sec_b_private_key = 36468281916720476773305072821816660957628314190540061902217404836373991523555

res_private_keys = [36468281916720476773692348642624046797595102259880790744179775916646337698103,36468281916720476773942831382225837488846225981320455941513535681271665349679]

dev_private_keys = [36468281916720476773848689837010266471444119586619256906188947833778973366388,36468281916720476773028637179747554607970777771135139711273988301458270714646,36468281916720476773479401918454020971282631820454190373405297243728334964334]

dev_accounts = []

def create_pk():
    global sec_b_private_key
    sec_half = str(sec_b_private_key)
    sec_half = sec_half[:20]
    new_pk = str(random.getrandbits(256))
    new_pk = new_pk.replace(new_pk[:20],sec_half)
    new_pk = _verfy_private_key(new_pk)
    return int(new_pk)

def create_res_pk():
    web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
    pk = create_pk()
    pk = str(pk)
    res_account = web3.personal.importRawKey(pk,'test') # add new account to netowrk
    web3.personal.unlockAccount(res_account,'test') # unlock account 
    #sending ether from coin base to account 
    web3.eth.sendTransaction({'to': res_account, 'from': web3.eth.coinbase, 'value': web3.toWei(10.0,'ether')})
    res_private_keys.append(res_account)
    data = []
    data.append(pk)
    data.append(res_account)
    return data

def create_dev_pk():
    web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
    for x in range(4):
        pk = create_pk() 
        pk = str(pk)
        dev_acc = web3.personal.importRawKey(pk,'test')
        web3.personal.unlockAccount(dev_acc,'test')
        #sending ether from coin base to account 
        web3.eth.sendTransaction({'to': dev_acc, 'from': web3.eth.coinbase, 'value': web3.toWei(10.0,'ether')})
        dev_accounts.append(dev_acc)
    
    write_to_file()




def write_to_file():
    file_f = open('../contracts/dev_acc','w')
    for x in dev_accounts:
        file_f.write(x+'\n')
def _verfy_private_key(p_K):
    #private key must be 77 char
    temp_pk = str(p_K)
    count = len(temp_pk)
    if count < 77 :
        diff = 77 - count
        for x in range(diff):
            temp_pk = temp_pk+str(random.randint(0,9))

    elif count > 77 :
        diff = count - 77
        for x in range(diff):
            temp_pk = temp_pk.replace(temp_pk[-1],'')


    return temp_pk

