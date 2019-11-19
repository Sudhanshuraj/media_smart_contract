import sys
import time
import pprint
import json
import random
import os
from eth_keys import keys
from ecies import encrypt, decrypt

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

def init_contract(address):
    contract_source_path = root + '/mediaContract.sol'

    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin'])
    return sort_contract

# send transaction for the user registration
def registerUser(userID, isConsumer, isCreator, userAddress, pubkey, address):
    sort_contract = init_contract(address)
    userCount1 = sort_contract.functions.getUserCount().call()
    tx_hash1 = sort_contract.functions.registerUser(userID, isConsumer, isCreator, userAddress, pubkey).transact({'txType':"0x1", 'from':w3.eth.accounts[0], 'gas':2409638})
    receipt1 = w3.eth.getTransactionReceipt(tx_hash1)

    while ((receipt1 is None)) : 
        time.sleep(1)
        receipt1 = w3.eth.getTransactionReceipt(tx_hash1)

    receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
    
    userCount2 = sort_contract.functions.getUserCount().call()
    
    if userCount1 == userCount2:
    	return "User with this userId already Exist"
    
    if receipt1 is not None:
        print("media:{0}".format(receipt1['gasUsed']))
        print("User Registered")
    return "Done"

#send getcall to fetch the media details
def getMedia(userId, address):
    sort_contract = init_contract(address)
    isConsumer = sort_contract.functions.isConsumer(userId).call()
    if not isConsumer:
        return "Function Not available for you\n"

    mediaCount = sort_contract.functions.getMediaCount().call()
    print("Total number of medias available: %d"%(mediaCount))
    for i in range(mediaCount):
        media = sort_contract.functions.getMediaByIndex(i).call()
        print("MediaID = %d"%(media[0]))
        # print("MediaID = %d, Creator UserID = %d"%(media[0], media[2]))
    return "Done"

def getMediaByID(mediaId, address):
    sort_contract = init_contract(address)
    media = sort_contract.functions.getMediaDetailsByID(mediaId).call()
    return media

def getUserByID(userId, address):
    sort_contract = init_contract(address)
    user = sort_contract.functions.getUserDetailsByID(userId).call()
    return user

    # print() # you may have to properly decode the result as the function will is returning the list
def getMediaDetails(address, _print=True):
    sort_contract = init_contract(address)

    mediaCount = sort_contract.functions.getMediaCount().call()
    print("Total number of medias available: %d"%(mediaCount))
    for i in range(mediaCount):
        media = sort_contract.functions.getMediaByIndex(i).call()
        print("MediaID = %d, Creator UserID = %d, Cost = %f, Info = %s"%(media[0], media[2], media[1], media[3]))
    return "Done"

def sendEther(sender, receiver, value):
	w3.eth.sendTransaction({'to':w3.toChecksumAddress(receiver), 'from':w3.toChecksumAddress(sender), 'value':w3.toWei(value, "ether")})
	return "Done"


def addMedia(userId, mediaId, cost, info, address):
    sort_contract = init_contract(address)

    isCreator = sort_contract.functions.isCreator(userId).call()
    if not isCreator:
        return "Function Not available for you\n"
    
    mediaCount1 = sort_contract.functions.getMediaCount().call()

    tx_hash = sort_contract.functions.addMedia(userId, mediaId, cost, info).transact({'txType':"0x1", 'from':w3.eth.accounts[0], 'gas':2409638})
    receipt1 = w3.eth.getTransactionReceipt(tx_hash)

    while ((receipt1 is None)) : 
        time.sleep(1)
        receipt1 = w3.eth.getTransactionReceipt(tx_hash)

    mediaCount2 = sort_contract.functions.getMediaCount().call()

    if mediaCount1 == mediaCount2:
    	return "Media with this Id already Exist"
    if receipt1 is not None:
        print("media:{0}".format(receipt1['gasUsed']))
        print("Media Added")
    return "Done"

def getCreator(userID, address):
    sort_contract = init_contract(address)
    isConsumer = sort_contract.functions.isConsumer(userID).call()
    if not isConsumer:
        return "Function Not available for you\n"
    userCount = sort_contract.functions.getUserCount().call()
    for i in range(userCount):
        [userId, isCreator, isConsumer, user_address] = sort_contract.functions.getUserByIndex(i).call()
        if isCreator:
            print("UserId = %d, UserAddress = %s"%(userId, user_address))
    return "Done"

def getConsumer(userID, address):
    sort_contract = init_contract(address)
    isCreator = sort_contract.functions.isCreator(userID).call()
    if not isCreator:
        return "Function Not available for you\n"
    userCount = sort_contract.functions.getUserCount().call()
    for i in range(userCount):
        [userId, isCreator, isConsumer, user_address] = sort_contract.functions.getUserByIndex(i).call()
        if isConsumer:
            print("UserId = %d, UserAddress = %s"%(userId, user_address))
    return "Done"

def purchaseMedia(userId, mediaId, address):
    sort_contract = init_contract(address)
    isConsumer = sort_contract.functions.isConsumer(userId).call()
    if not isConsumer:
        return "Function Not available for you\n"

    mediaBuyer = sort_contract.functions.getMediaBuyer(mediaId).call()
    if userId in mediaBuyer:
        return "Media already bought by the user\n"
    else:
        media = getMediaByID(mediaId, address)
        user = getUserByID(userId, address)
        if userId == media[2]:
        	return "Owner Can't buy his own Media"
        receiver = getUserByID(media[2], address)[3]
        sender = user[3]
        balance = w3.fromWei(w3.eth.getBalance(w3.toChecksumAddress(sender)), "ether")
        if balance < media[1]:
        	return "Not Sufficient Balance"
        sendEther(sender, receiver, media[1])
        tx_hash = sort_contract.functions.addBuyerForMedia(userId, mediaId).transact({'txType':"0x1", 'from':w3.eth.accounts[0], 'gas':2409638})
        receipt1 = w3.eth.getTransactionReceipt(tx_hash)

        while ((receipt1 is None)) : 
            time.sleep(1)
            receipt1 = w3.eth.getTransactionReceipt(tx_hash)
        if receipt1 is not None:
            print("media:{0}".format(receipt1['gasUsed']))
            print("Media Bought")
        mediaBuyer = sort_contract.functions.getMediaBuyer(mediaId).call()
        if userId in mediaBuyer:
            return "Done"

def sendMediaLink(userId, destId, mediaId, address):
	sort_contract = init_contract(address)
	isCreator = sort_contract.functions.isCreator(userId).call()
	if not isCreator:
		return "Function Not available for you\n"

	mediaBuyer = sort_contract.functions.getMediaBuyer(mediaId).call()
	if destId not in mediaBuyer:
		return "Media not bought by the user\n"

	mediaAlreadyHave = sort_contract.functions.getMediaAlreadyHave(mediaId).call()
	if destId in mediaAlreadyHave:
		return "Media Link already sent to the user\n"

	sender_user = getUserByID(userId, address)
	receiver_user = getUserByID(destId, address)
	sender_address = sender_user[3]
	receiver_address = receiver_user[3]

	receiver_pubkey = receiver_user[4]

	mediaURL = str(random.randrange(1,100000))
	mediaURL_encrypted = encrypt(receiver_pubkey, mediaURL.encode())
	mediaURL_encrypted = "".join(["{:02X}".format(c) for c in mediaURL_encrypted])


	# w3.eth.sendTransaction({'to':w3.toChecksumAddress(receiver), 'from':w3.toChecksumAddress(sender), 'value':w3.toWei(0, "ether"), 'data':w3.toHex(mediaURL.encode())})
	
	tx_hash = sort_contract.functions.sendMediaLink(userId, destId, mediaId, str(mediaURL_encrypted)).transact({'txType':"0x1", 'from':w3.eth.accounts[0], 'gas':2409638})
	receipt1 = w3.eth.getTransactionReceipt(tx_hash)

	while ((receipt1 is None)) : 
	    time.sleep(1)
	    receipt1 = w3.eth.getTransactionReceipt(tx_hash)
	if receipt1 is not None:
	    print("media:{0}".format(receipt1['gasUsed']))
	    print("Link Sent")

	return "Done"

def getMediaURL(userId, mediaId, address):
	sort_contract = init_contract(address)
	mediaURL_encrypted = sort_contract.functions.getMediaURL(userId, mediaId).call()
	if "Error" in mediaURL_encrypted:
		return mediaURL_encrypted
	mediaURL_encrypted = bytes.fromhex(mediaURL_encrypted)

	mediaURL_decrypted = decrypt(prv_key, mediaURL_encrypted)
	print("Media Url for Media ID %d = %s"%(mediaId, mediaURL_decrypted.decode()))
	return "Done"




w3 = Web3(IPCProvider(root + '/test-eth%d/geth.ipc'%(user), timeout=100000))

address = "NULL"
with open(root + '/contractAddressList1') as fp:
    for line in fp:
        a,b = line.rstrip().split(':', 1)
        if a == "media":
            address = b
for x in os.listdir(root + '/test-eth%d/keystore/'%(user)):
    if (w3.eth.accounts[0][2:]).lower() in x:
        file = x 
password = (open('password.txt', 'r')).read()
with open(root + '/test-eth%d/keystore/%s'%(user, file)) as keyfile:
    encrypted_key = keyfile.read()
    prv_key = w3.eth.account.decrypt(encrypted_key, password)
    pub_key = str((keys.PrivateKey(prv_key)).public_key)

while True:
    function = input("What do you want to do?\n")
    if function == "registerUser":
        userId = int(input("Enter UserID: "))
        isConsumer = True if input("isConsumer(y or n): ") == 'y' else False
        isCreator = True if input("isCreator(y or n): ") == 'y' else False
        user_address = w3.eth.accounts[0]
        try:
        	print(registerUser(userId, isConsumer, isCreator, user_address, pub_key, address))
        except Exception as e:
        	print(e)
    elif function == "addMedia":
        userId = int(input("Enter UserID: "))
        mediaId = int(input("Enter MediaId: "))
        cost = int(input("Enter cost: "))
        info = input("Enter info about Media: ")
        try:
        	print(addMedia(userId, mediaId, cost, info, address))
        except Exception as e:
        	print(e)
    elif function == "getMedia":
        userId = int(input("Enter UserID: "))
        print(getMedia(userId, address))
    elif function == "getMediaDetails":
        try:
        	print(getMediaDetails(address))
        except Exception as e:
        	print(e)
    elif function == "getCreator":
        userId = int(input("Enter UserID: "))
        try:
        	print(getCreator(userId, address))
        except Exception as e:
        	print(e)
    elif function == "getConsumer":
        userId = int(input("Enter UserID: "))
        try:
        	print(getConsumer(userId, address))
        except Exception as e:
        	print(e)
    elif function == "purchaseMedia":
        userId = int(input("Enter UserID: "))
        mediaId = int(input("Enter MediaId: "))
        try:
        	print(purchaseMedia(userId, mediaId, address))        
        except Exception as e:
        	print(e)
    elif function == "sendMediaLink":
    	userId = int(input("Enter UserID: "))
    	destId = int(input("Enter Destination User ID: "))
    	mediaId = int(input("Enter MediaId: "))
    	try:
    		print(sendMediaLink(userId, destId, mediaId, address))
    	except Exception as e:
    		print(e)
    elif function == "getMediaUrl":
    	userId = int(input("Enter UserID: "))
    	mediaId = int(input("Enter MediaId: "))
    	try:
    		print(getMediaURL(userId, mediaId, address))
    	except Exception as e:
    		print(e)
    elif function == "exit":
    	print("Exiting....")
    	exit()
    else:
        print("Invalid Function\nTry Again\n")

