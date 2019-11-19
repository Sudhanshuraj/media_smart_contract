#How to Run
- Put all the required files in a folder
- Open config.json file and replace the path according to the setup
- open openhelhers file and modify the paths
- open startIpc file and modify the paths 
- Run the openhelpers file
- Run `python3 deployContact.py [1/2/3]`. [1/2/3] represents the user which will deploy the contract. 
- Run `python3 sendTransaction.py [1/2/3]`. [1/2/3] represents the user which will do the transactions.
- After running sendTransaction.py, It will ask "What do you want to do?". Possible options are:
	- registerUser
	- addMedia
	- getMedia
	- getMediaDetails
	- getCreator
	- getConsumer
	- purchaseMedia
	- sendMediaLink
	- getMediaUrl
- The above options are self explanatory.
- Type one of the options and press enter.
- It will ask some questions depending upon the option selected.
- Answer the questions and you are good to go.


#Explaining The Code
- `mediaContract.sol` contains the contract which is to be deployed.
- `sendTransaction.py` contains the frontend for executing the transaction for various operations.
- All the functions are implemented as per the problem statement.
- Some helper functions have also been introduced as per convenience.
