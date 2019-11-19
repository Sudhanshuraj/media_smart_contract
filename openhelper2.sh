# !/bin/bash
root="/home/sudhanshu/Documents/Assignment3"
geth_root="$root""/go-ethereum/build/bin/geth"
rm -r "$root"/test-eth2/geth/chaindata/;
rm -r "$root"/test-eth2/geth/lightchaindata/;
rm -r "$root"/test-eth2/geth/nodes/;
rm -r "$root"/test-eth2/geth/ethash/;
rm "$root"/test-eth2/geth/LOCK;
rm "$root"/test-eth2/geth/transactions.rlp;
"$geth_root" --datadir "$root"/test-eth2 --rpc --rpcport=1598 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1587  --syncmode full --gcmode archive --nodiscover --nodekey nk2.txt init "$root"/genesis.json
gnome-terminal --geometry 90x25+1300+50 -- bash startIpc.sh 2
"$geth_root" --datadir "$root"/test-eth2 --rpc --rpcport=1598 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1587  --syncmode full --gcmode archive --nodiscover --nodekey nk2.txt --verbosity 5 --allow-insecure-unlock --unlock 0,1 --password password.txt 

# "$root"/Assignment-go-ethereum/build/bin/geth --datadir "$root"/test-eth2 --rpc --rpcport=1598 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1587 --hashpower 50 --interarrival 2 --behavior 0 --gcmode archive --nodekey=nk2.txt init "$root"/genesis.json
# gnome-terminal --geometry 90x25+1300+50 -- bash startIpc.sh 2
# "$root"/Assignment-go-ethereum/build/bin/geth --datadir "$root"/test-eth2 --rpc --rpcport=1598 --rpcapi "eth,net,web3,debug" --networkid=1748 --port=1587 --hashpower 50 --interarrival 2 --behavior 0 --gcmode archive --nodekey=nk2.txt --verbosity 3 --allow-insecure-unlock --unlock 0,1 --password password.txt