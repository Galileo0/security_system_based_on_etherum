from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json



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


def edit_access(email,duration,days,pk):
    # ----- res account ----- #
    web3.eth.defalutAccount = pk
    #------ End-----#
    transact = contract.functions.edit_worker_access(email,duration,days).transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().edit_worker_access(email,duration,days)
    result = str(result)
    return result