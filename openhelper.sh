# !/bin/bash
root="/home/sudhanshu/Documents/Assignment3"
geth_root="$root""/go-ethereum/build/bin/geth"
rm -r "$root"/test-eth1/geth/chaindata/;
rm -r "$root"/test-eth1/geth/lightchaindata/;
rm -r "$root"/test-eth1/geth/nodes/;
rm -r "$root"/test-eth1/geth/ethash/;
rm "$root"/test-eth1/geth/LOCK;
rm "$root"/test-eth1/geth/transactions.rlp;
"$geth_root" --datadir "$root"/test-eth1 --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey nk1.txt init "$root"/genesis.json
gnome-terminal --geometry 90x25+1300+1550 -- bash startIpc.sh 1
"$geth_root" --datadir "$root"/test-eth1 --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1547  --syncmode full --gcmode archive --nodiscover --nodekey nk1.txt --verbosity 5 --allow-insecure-unlock --unlock 0,1 --password password.txt 

#/home/nitin14/AssignmentSetup/Assignment-go-ethereum/build/bin/geth --datadir /home/nitin14/AssignmentSetup/test-eth1 --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1547 --hashpower 50 --interarrival 2 --behavior 0 --gcmode archive --nodekey=nk.txt init /home/nitin14/AssignmentSetup/genesis.json
#gnome-terminal --geometry 90x25+1300+1550 -- bash startIpc.sh 1
#/home/nitin14/AssignmentSetup/Assignment-go-ethereum/build/bin/geth --datadir /home/nitin14/AssignmentSetup/test-eth1 --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1547 --hashpower 50 --interarrival 2 --behavior 0 --gcmode archive --nodekey=nk.txt --verbosity 3 --allow-insecure-unlock --unlock 0,1 --password password.txt