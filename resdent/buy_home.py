from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json




web3 = Web3(HTTPProvider('http://192.168.43.23:8545'))
con_abi = open('../contracts/con_abi','r')
con_abi = con_abi.read()
con_add = open('../contracts/con_add','r')
con_add = con_add.read()
con_byte_code = open('../contracts/con_byte_code','r')
con_byte_code = con_byte_code.read() 
con_add = web3.toChecksumAddress(con_add)
bid_abi=json.loads(con_abi)
contract = web3.eth.contract(abi=con_abi,address = con_add)

home = []

def get_home(pk):
    web3.eth.defalutAccount = pk 
    transact = contract.functions.get_home_count().transact({'from': web3.eth.defalutAccount}) # transaction
    result = contract.call().get_home_count()
    home_count = int(result)

    if home_count == 0 :
        home.append('No Avalible Home For Sell')
    else:
        for x in range(1,(home_count+1)):
            transact = contract.functions.get_sell_home(x).transact({'from': web3.eth.defalutAccount}) # transaction
            data = contract.call().get_sell_home(x)
            data = str(data)
            home.append(data)
            print(data)
    
    return home
