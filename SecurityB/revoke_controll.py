from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json

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

def revoke(_email):
    transact = contract.functions.revoke_res(_email,1).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().revoke_res(_email,1)
    result = str(result)

    if result == '1':
        return 1
    elif result == '0':
        transact = contract.functions.revoke_visitor(_email,1).transact({'from': web3.eth.defalutAccount}) # transaction
        result = contract.call().revoke_visitor(_email,1)
        result = str(result)
        if result == '1':
            return 1
        elif result == '0':
            transact = contract.functions.revoke_worker(_email,1).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().revoke_worker(_email,1)
            result = str(result)
            return result 


def unrevoke(_email):
    transact = contract.functions.revoke_res(_email,0).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().revoke_res(_email,0)
    result = str(result)

    if result == '1':
        return 1
    elif result == '0':
        transact = contract.functions.revoke_visitor(_email,0).transact({'from': web3.eth.defalutAccount}) # transaction
        result = contract.call().revoke_visitor(_email,0)
        result = str(result)
        if result == '1':
            return 1
        elif result == '0':
            transact = contract.functions.revoke_worker(_email,0).transact({'from': web3.eth.defalutAccount}) # transaction
            result = contract.call().revoke_worker(_email,0)
            result = str(result)

            return result 

