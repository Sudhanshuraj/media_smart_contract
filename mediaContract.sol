pragma solidity ^0.4.24;
pragma experimental ABIEncoderV2;

contract mediaContract {
  	int public  mediaCount; /*you should remove this variable, this just used to assign value*/
  	int public  userCount;

    /*Data structure for user-consumer(individual or company) or creator*/
	struct userInfo {
	    int userId;
	  	bool isConsumer;
	  	bool isCreator;
        string user_address;
        string public_key;
        mapping(int => string) mediasForUser;
	}
	mapping(int => userInfo) users;
	int[] public userIds;

	/*	You are free to add or remove field from userInfo structure in case required.
	*/
    /*Data structure for Media*/
	struct mediaInfo {
	    int mediaId;	  	
        int[] usersBought;
        int[] usersAlreadyHave;
        int ownerUserId;
        int cost;
        string info;
        // string mediaURL;
	  	
	}
	mapping(int => mediaInfo) mediaLicenses;
	int[] public mediaIds;


    constructor() public {
        mediaCount = 0;
        userCount = 0;
        // dummy1 = dummy2; /*you should define by replacing dummies with proper variables*/
    }
    /*Register the user in the smart contract (DAPP). This function is accessible to
    both creator and consumer*/
	function registerUser(int  userId, bool  isConsumer, bool  isCreator, string user_address, string public_key) public {
		for( uint i = 0; i < uint(userCount); i++){
			if (userIds[i] == userId){
				return;
			}
		}
        userInfo storage newUser = users[userId];
        newUser.userId = userId;
        newUser.isConsumer = isConsumer;
        newUser.isCreator = isCreator;
        newUser.user_address = user_address;
        newUser.public_key = public_key;
        userIds.push(userId);
        userCount++;
    }
  
    /*Add the media to smart contracts with the list of stakeholders, the owner(creator)
    info, stakeholder shares, the price they are offering for an individual and a company, etc. This function should be accessible to the creator only*/
    function addMedia(int owner, int mediaId, int cost, string info) public {
    	if (isCreator(owner) == false){
    		return;
    	}
    	for( uint i = 0; i < uint(mediaCount); i++){
			if (mediaIds[i] == mediaId){
				return;
			}
		}
        mediaInfo storage newMedia = mediaLicenses[mediaId];
        newMedia.cost = cost;
        newMedia.mediaId = mediaId;
        newMedia.info = info;
        // newMedia.mediaURL = mediaURL;
        newMedia.ownerUserId = owner;
        mediaIds.push(mediaId);
        mediaCount++;
    	/*you should use proper structure variable that you are going to define, instead of dummy*/
    	/*code to add media to contract*/
    }

    /*It transfers the purchase amount from the consumer to the creator account.
    Please make sure to distinguish between the individual consumer and the company while charging the amount. Also, this function should ensure the availability of balance in the consumer’s account. This function should be exposed to the consumer only*/
    function purchaseMedia(int mediaId, int userId) public {
    	if (isConsumer(userId) == false){
    		return;
    	}
        (mediaLicenses[mediaId]).usersBought.push(userId);
    	/*you should use proper structure variable that you are going to define, instead of dummy*/
    	/*code to purchase media to contract*/
    }

    function getMediaCount() public view returns (int MediaCount){
        return mediaCount;
    }

    function getMediaURL(int userId, int mediaId) public view returns (string){
    	mediaInfo memory media = mediaLicenses[mediaId];
    	bool check = false;
    	for (uint i = 0; i < (media.usersAlreadyHave).length; i++){
    		if ((media.usersAlreadyHave)[i] == userId){
    			check = true;
    		}

    	}
    	if (check == false){
    		return "Permission Error";
    	}
        return users[userId].mediasForUser[mediaId];
    }

    function getMediaDetailsByID(int mediaID) public view returns (int, int, int, string){
        mediaInfo memory media = mediaLicenses[mediaID];
        return (media.mediaId, media.cost, media.ownerUserId, media.info);
    }

    function getMediaByIndex(int index) public view returns (int, int, int, string){
        mediaInfo memory media = mediaLicenses[mediaIds[uint(index)]];
        return (media.mediaId, media.cost, media.ownerUserId, media.info) ;
    }

    function getUserCount() public view returns (int UserCount){
        return userCount;
    }

    function getUserDetailsByID(int userId) public view returns (int, bool, bool, string, string){
        userInfo memory user = users[userId];
        return (user.userId, user.isCreator, user.isConsumer, user.user_address, user.public_key);
    }

    function getUserByIndex(int index) public view returns (int, bool, bool, string){
        userInfo memory user = users[userIds[uint(index)]];
        return (user.userId, user.isCreator, user.isConsumer, user.user_address);
    }

    function getMediaBuyer(int mediaID) returns (int[]){
        return mediaLicenses[mediaID].usersBought;
    } 

    function getMediaAlreadyHave(int mediaId) returns (int []){
    	return mediaLicenses[mediaId].usersAlreadyHave;
    }

    function getMediaServedUsers(int mediaID) returns (int[]){
        return mediaLicenses[mediaID].usersAlreadyHave;
    } 

    function addBuyerForMedia(int userID, int mediaID) {
    	if (isConsumer(userID) == false){
    		return;
    	}
        (mediaLicenses[mediaID].usersBought).push(userID);
    }

    /*Randomly generate the url here and send it to the consumer after encrypting it with the consumer’s public key. Before sending the url to the consumer,you should ensure that the payment made by him is confirmed (payment transaction is encapsulated in some block). This function should be accessible to the creator only*/
    function sendMediaLink(int userId, int destId, int mediaId, string mediaLink) {
    	if (isCreator(userId) == false || isConsumer(destId) == false){
    		return;
    	}
    	mediaInfo memory media = mediaLicenses[mediaId];
    	bool check = false;
    	for (uint i = 0; i < (media.usersBought).length; i++){
    		if ((media.usersBought)[i] == destId){
    			check = true;
    		}

    	}
    	if (check == true){
        	(mediaLicenses[mediaId].usersAlreadyHave).push(destId);
            users[destId].mediasForUser[mediaId] = mediaLink;
            
    	}
    	/*you should use proper structure variable that you are going to define, instead of dummy*/
    	/*code to sendMediaLink media to contract*/
    }

    function isCreator(int userId) returns(bool){
        userInfo memory user = users[userId];
        return user.isCreator;
    }

    function isConsumer(int userId) returns(bool){
        userInfo memory user = users[userId];
        return user.isConsumer;
    }
}