import sys
import time
import pprint
import json

from web3 import *
from solc import compile_source

# root = "/home/sudhanshu/Documents/Assignment3"
config = json.loads(open('config.json').read())
root = config['root']

user = int(sys.argv[1])

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def read_address_file(file_path):
    file = open(file_path, 'r')
    addresses = file.read().splitlines() 
    return addresses


def connectWeb3():
    return Web3(IPCProvider(root + '/test-eth%d/geth.ipc'%(user), timeout=100000))

#Deploy the DAPP for media distribution.
def deployMediaContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface1 = compiled_sol.popitem()
    tx_hash = w3.eth.contract(
            abi=contract_interface1['abi'],
            bytecode=contract_interface1['bin']).constructor().transact({'txType':"0x0", 'from':account, 'gas':8500000})
    return tx_hash

#instead of 42 you have to send the required variables.

def deployContracts(w3, account):
    tx_hash1 = deployMediaContract(media_source_path, w3, account)
    receipt1 = w3.eth.getTransactionReceipt(tx_hash1)

    while ((receipt1 is None)):
        time.sleep(1)
        receipt1 = w3.eth.getTransactionReceipt(tx_hash1)

    # w3.miner.stop()

    if receipt1 is not None:
        print("media:{0}".format(receipt1['contractAddress']), file=open(root + '/contractAddressList1', 'w'))
    print("DONE")

media_source_path = root + '/mediaContract.sol'

w3 = connectWeb3()
w3.miner.start(1)
# time.sleep(24)
deployContracts(w3, w3.eth.accounts[0])