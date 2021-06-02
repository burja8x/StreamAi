pragma solidity ^0.6.12;
//pragma abicoder v2;
pragma experimental ABIEncoderV2;

import "https://raw.githubusercontent.com/smartcontractkit/chainlink/master/evm-contracts/src/v0.6/ChainlinkClient.sol";
import "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/solc-0.6/contracts/access/Ownable.sol";

contract SafeMath {
    function safeMul(uint a, uint b) internal pure returns (uint) {
        uint c = a * b;
        require(a == 0 || c / a == b);
        return c;
    }
    
    function safeSub(uint a, uint b) internal pure returns (uint) {
        require(b <= a);
        return a - b;
    }
    
    function safeAdd(uint a, uint b) internal pure returns (uint) {
        uint c = a + b;
        require(c >= a && c >= b);
        return c;
    }
}

contract AiPlatforma is SafeMath, ChainlinkClient, Ownable {

	struct CProvider{
		string name;
		bool Allowed;

		uint32 maxRam;
		uint24 maxCpus;
		uint24 maxGpus;
		uint24 maxRunning;
		
		uint32 usedRam;
        uint24 usedCpus;
        uint24 usedGpus;
        uint24 usedInstances;
		
		//bool exist;
		uint32 id;
		address addr;
	}

	struct AiMethod{
		address creator;
		string name;
		uint32 ram;
		uint24 cpu;
		bool gpuRequired;
		uint price;
		bool Allowed;
		bool Active;
		string ipfsCID;
		bool onlyAllowedUsers;
		uint32 id;
	}
	
	struct LockedFunds {
	    uint ethProvider;
	    address provider;
	    uint ethAiCreator;
	    address aiCreator;
	    uint ethFee;
	    uint32 releaseBlock;
	    address buyer;
	    uint32 timeInSec;
	    uint32 methodId;
	    bool complaintWritten;
	}

    bool public useOracle = false;
    
	uint32 public methodCounter = 0;
	uint32 public dealIdCounter = 0;
	uint32 public hostCounter = 1;

	uint32 public waitNumberOfBlocksBeforeStart = 5;
	uint32 public waitNumberOfBlocksAfterStart = 5;

	address public admin;
	address public feeAccount;

	mapping (address => CProvider) public hosts;
	mapping (uint32 => address) public hostsIndex; // easy way to find providers (allowed providers)
	mapping (uint32 => AiMethod) public aiMethods;
    mapping (uint32 => mapping(address => uint)) providersPrice;

	uint public feeMake; // pay -> ai method creator
	uint public feeTake; // % to platform.
	uint24 public minTime = 10; // minimalen čas zakupa Ai.
	uint24 public maxTime = 10000000;

	mapping (address => uint) public eth;
	mapping (uint32 => LockedFunds) public locked;

    /* oracle */
    uint256 public oracleFee;
    //uint256 public currentPrice;
    string public url0;
    string public url1;
    address public oracleAddr;
    bytes32 public jobId;
    
    struct RequestIdToUser{
        address user;
        uint32 method_id;
    }
    
    mapping (bytes32 => RequestIdToUser) public rToU;
    mapping (uint32 => mapping(address => bool)) allowUserToBuy;
    
    event LogAskOracle(address fromUser, uint amount, bytes data);
    /* */

	event Withdraw(address user, uint amount);
	event BuyAi(address userBuying, uint32 aiMethodId, address provider, uint containerPrice, uint aiMethodPrice, uint24 timeInSec, uint32 dealId, string videoStreamUrl);
	event SellAi(address userSelling, string name, uint32 aiMethodId, uint price, uint32 ram, uint24 cpus, bool gpu, string ipfsCID, bool onlyAllowedUsers, string dockerHubLink);
    event Start(uint32 dealId, string ECmqttLink);
    event End(uint32 dealId, bool error);
    event Complaint(uint32 dealId, string text);
    event ContainerCost(uint32 aiMethodId, address provider, uint containerCost);
    event MethodCost(uint32 aiMethodId, uint methodCost);

	//constructor(uint feeMake_, uint16 feeTake_) internal {
	constructor() public {
	    admin = msg.sender;
	    feeAccount = msg.sender;
	    // feeMake = feeMake_; // eth
	    // feeTake = feeTake_; // % * 1000
	    feeMake = 1200000;
	    feeTake = 18; // = 1,8%
	    
	    /* oracle */
	    setPublicChainlinkToken();
        url0 = "https://API_URL.com/api/v1/account/isAiMethodAllowedForUser?aiMethodId=";
        url1 = "&userEthAddress=";
        oracleAddr = 0x56dd6586DB0D08c6Ce7B2f2805af28616E082455;
        jobId = "1b2658f2d679437cb2d8db115c646d02";
        oracleFee = 1e17;
	}

	modifier onlyAdmin(){
		require(msg.sender == admin);
		_;
	}

    function changeAskUrl(string memory url0_, string memory url1_) public onlyAdmin{
        url0 = url0_;
        url1 = url1_;
    }
    
    function changeOracle(address oracleAddr_, uint oracleFee_, bytes32 jobId_) public onlyAdmin{
        oracleAddr = oracleAddr_;
        oracleFee = oracleFee_;
        jobId = jobId_;
    }

	function changeAdmin(address admin_) public onlyAdmin{
   		admin = admin_;
	}
	
	function changeFeeAccount(address feeAccount_) public onlyAdmin{
		feeAccount = feeAccount_;
	}

	function changeUserChecker(bool useOracle_) public onlyAdmin{
		useOracle = useOracle_;
	}
	
	function allowUserToUseMethod(uint32 method_id_, address user_, bool allow_) public onlyAdmin{
	    allowUserToBuy[method_id_][user_] = allow_;
	}
    
    function changeWaitTime(uint32 waitNumberOfBlocksBeforeStart_, uint32 waitNumberOfBlocksAfterStart_) public onlyAdmin{
   		waitNumberOfBlocksBeforeStart = waitNumberOfBlocksBeforeStart_;
   		waitNumberOfBlocksAfterStart = waitNumberOfBlocksAfterStart_;
	}

	function changeFeeMake(uint feeMake_) public onlyAdmin{
		feeMake = feeMake_;
	}

	function changeFeeTake(uint16 feeTake_) public onlyAdmin{
        require(feeTake_ < 500); // manše od 50%      0.5 = (/ 1000) * 500
		feeTake = feeTake_;
	}

    function allowCProvider(address provider_, bool allow_) public onlyAdmin{  	
    	CProvider storage host = hosts[provider_];
    	require(host.addr != address(0), "Provider does not exist.");
		host.Allowed = allow_;
	}
	
	function allowAiMethod(uint32 ai_method_id_, bool allow_) public onlyAdmin{
		AiMethod storage method = aiMethods[ai_method_id_];
		require(method.ram != 0, "Method does not exist.");
		method.Allowed = allow_;
	}
	
	// Start after confermation time (10 blocks). ???????????????????????????
	function start(uint32 dealId_, string memory ECmqttLink_) public onlyAdmin{
	    
	    // MQTT link encrypted with buyer address.
	    LockedFunds memory funds = locked[dealId_];
	    require(funds.releaseBlock != 0, "This dealId does not exist.");
	    require(funds.ethFee + funds.ethProvider + funds.ethAiCreator != 0, "No locked funds found."); // if user took eth
	    
	    funds.releaseBlock = uint32(block.number + (funds.timeInSec / 13) + waitNumberOfBlocksAfterStart);
	    
        emit Start(dealId_, ECmqttLink_);
	}

	function delivered(uint32 dealId_, bool error_) public onlyAdmin{
	    LockedFunds memory funds = locked[dealId_];
	    require(funds.releaseBlock != 0, "This dealId does not exist or no funds."); // if exist
        require(funds.ethFee + funds.ethProvider + funds.ethAiCreator != 0, "No locked funds found.");
        
        if(error_){
            returnToBuyer(dealId_);
        }else{
            releaseFunds(dealId_);
        }
        
        //release CPU, RAM, GPU and instance.
        releaseResources(funds.provider, funds.methodId);
        
        emit End(dealId_, error_);
	}
	
	//----------------------------- Provider
	
	function newCProvider(string memory name_, uint32 maxRam_, uint24 maxCpus_, uint24 maxGpus_, uint24 maxRunning_) public {
		require(hosts[msg.sender].addr == address(0), "Provider already exist.");
		hosts[msg.sender] = CProvider(name_, false, maxRam_, maxCpus_, maxGpus_, maxRunning_, 0, 0, 0, 0, 0, msg.sender);
		hostCounter += 1;
        hostsIndex[hostCounter] = msg.sender;
        hosts[msg.sender].id = hostCounter;
	}

	function changeCProviderData(uint32 maxRam_, uint24 maxCpus_, uint24 maxGpus_, uint24 maxRunning_) public{
    	CProvider storage host = hosts[msg.sender];
		require(host.id != 0, "Provider does not exist.");
		host.maxRam = maxRam_;
		host.maxCpus = maxCpus_;
		host.maxGpus = maxGpus_;
		host.maxRunning = maxRunning_;
	}

	function setContainerCost(uint32 ai_method_id_, uint containerCost_) public{
		CProvider memory host = hosts[msg.sender];
		AiMethod memory method = aiMethods[ai_method_id_];
		require(host.Allowed && method.ram != 0, "Provider not allowed or method does not exist.");
		if(containerCost_ == 0){
		    delete providersPrice[ai_method_id_][msg.sender];
		}else{
		    providersPrice[ai_method_id_][msg.sender] = containerCost_;
		}
		
		emit ContainerCost(ai_method_id_, msg.sender, containerCost_);
	}

    //---------------------------- seller
	function sell(string memory name_, uint32 ram_, uint24 cpus_, bool gpu_, uint price_, string memory ipfsCID_, bool onlyAllowedUsers_, string memory dockerHubLink_) public payable returns (uint32){
		require(msg.value >= feeMake, "Payment too small.");
		
		methodCounter += 1;
		aiMethods[methodCounter] = AiMethod(msg.sender, name_, ram_, cpus_, gpu_, price_, false, true, ipfsCID_, onlyAllowedUsers_, methodCounter);

		eth[feeAccount] += msg.value;

		emit SellAi(msg.sender, name_, methodCounter, price_, ram_, cpus_, gpu_, ipfsCID_, onlyAllowedUsers_, dockerHubLink_);
		
		return methodCounter;
	}
	
	function activateAiMethod(uint32 ai_method_id_, bool activate_) public{
		AiMethod storage method = aiMethods[ai_method_id_];
		require(method.creator == msg.sender, "Only method creator can change method status.");
		method.Active = activate_;
	}
	
	function changeAiMethodPrice(uint32 ai_method_id_, uint price_) public{
		AiMethod storage method = aiMethods[ai_method_id_];
		require(method.ram != 0, "This method does not exist.");
		require(method.creator == msg.sender, "Only method creator can modify method price.");
		method.price = price_;
		emit MethodCost(ai_method_id_, price_);
	}

    //---------------------------- Buyer
	
	function buy(uint32 ai_method_id_, address provider_, uint container_price_, uint ai_method_price_, uint24 timeInSec_, string memory videoStreamUrl_) public payable returns (uint32){
		AiMethod memory method = aiMethods[ai_method_id_];
		CProvider storage provider = hosts[provider_];
        require(provider.Allowed && method.Allowed && method.Active, "provider and method must be allowed and active.");
		require(providersPrice[ai_method_id_][provider_] == container_price_ && ai_method_price_ == method.price && container_price_ != 0, "maybe the price has changed.");
		require(timeInSec_ >= minTime && timeInSec_ <= maxTime, "timeInSec must be between minTime and maxTime!");
		
        uint tmp = safeMul(timeInSec_, safeAdd(container_price_, ai_method_price_));
        tmp = tmp + (safeMul(tmp,feeTake) / 1000);
        require(tmp <= msg.value, "not enough eth.");
        require(!method.onlyAllowedUsers || (method.onlyAllowedUsers && allowUserToBuy[ai_method_id_][msg.sender]), "User not allowed to buy this method. Read more in FAQ."); 
		uint ethToAiMethodCreator = safeMul(ai_method_price_, timeInSec_);
		uint ethToProvider = safeMul(container_price_, timeInSec_);
		uint32 waitUntil = uint32(block.number + waitNumberOfBlocksBeforeStart);
		
		dealIdCounter += 1;
		
		locked[dealIdCounter] = LockedFunds(ethToProvider, provider_, ethToAiMethodCreator, method.creator, safeSub(safeSub(msg.value, ethToAiMethodCreator), ethToProvider), waitUntil, msg.sender, timeInSec_, ai_method_id_, false);		
		
		// RAM, CPU, GPU reservation 
		provider.usedRam = uint32(safeAdd(provider.usedRam, method.ram));
		provider.usedCpus = uint24(safeAdd(provider.usedCpus, method.cpu));
		provider.usedInstances = uint24(safeAdd(provider.usedInstances, 1));
		if(method.gpuRequired){
		    provider.usedGpus = uint24(safeAdd(provider.usedGpus, 1));
		}
        require(provider.usedRam <= provider.maxRam && provider.usedCpus <= provider.maxCpus && provider.usedInstances <= provider.maxRunning && provider.usedGpus <= provider.maxGpus, "Currently provider does not have enough (ram or cpus gpu or or instances)");

		emit BuyAi(msg.sender, ai_method_id_, provider_, container_price_, ai_method_price_, timeInSec_, dealIdCounter, videoStreamUrl_);
        
		return dealIdCounter;
	}

	function complaint(uint32 dealId_, string memory text_) public{
        LockedFunds storage funds = locked[dealId_];
	    require(funds.releaseBlock != 0, "dealId not found.");
	    require(funds.buyer == msg.sender, "only buyer can write Complaint.");
	    require(funds.complaintWritten == false, "Complaint already written.");
	    funds.complaintWritten = true;
	    emit Complaint(dealId_, text_);
	}

    function returnToBuyerSAFU(uint32 dealId_) public{
		LockedFunds storage funds = locked[dealId_];
		require(funds.buyer == msg.sender, "only buyer can call this function.");
		require(block.number > funds.releaseBlock, "current block number must be bigger then releaseBlock.");
		require(funds.ethFee + funds.ethProvider + funds.ethAiCreator != 0, "No locked funds found.");
		
		returnToBuyer(dealId_);
		
        releaseResources(funds.provider, funds.methodId);
        
        emit End(dealId_, true);
	}
	
	// ----------------------------
	
	function releaseFunds(uint32 dealId_) private{
		LockedFunds storage funds = locked[dealId_];
	    require(funds.buyer != address(0), "no deal with this dealId.");
		uint ethProvider = funds.ethProvider;
		uint ethAiCreator = funds.ethAiCreator;
		uint ethFee = funds.ethFee;
		funds.ethProvider = 0;
		funds.ethAiCreator = 0;
		funds.ethFee = 0;
		eth[funds.provider] += ethProvider;
		eth[funds.aiCreator] += ethAiCreator;
		eth[feeAccount] += ethFee;
	}

    function releaseResources(address provider_, uint32 methodId_) private{
        CProvider storage provider = hosts[provider_];
        AiMethod memory method = aiMethods[methodId_];
        provider.usedRam = uint32(safeSub(provider.usedRam, method.ram));
		provider.usedCpus = uint24(safeSub(provider.usedCpus, method.cpu));
		provider.usedInstances = uint24(safeSub(provider.usedInstances, 1));
		if(method.gpuRequired){
		    provider.usedGpus = uint24(safeSub(provider.usedGpus, 1));
		}
    }
    
	function returnToBuyer(uint32 dealId_) private{
		LockedFunds storage funds = locked[dealId_];
	    require(funds.buyer != address(0), "no deal with this dealId.");
		uint ethProvider = funds.ethProvider;
		uint ethAiCreator = funds.ethAiCreator;
		uint ethFee = funds.ethFee;
		funds.ethProvider = 0;
		funds.ethAiCreator = 0;
		funds.ethFee = 0;
		eth[funds.buyer] += ethProvider;
		eth[funds.buyer] += ethAiCreator;
		eth[funds.buyer] += ethFee;
	}
	
	function getProviderPrice(uint32 ai_method_id_, address provider_) public view returns (uint){
		return providersPrice[ai_method_id_][provider_];
	}
	
	function getPricesOfProviders(uint32 ai_method_id_, address[] calldata providers_) public view returns (uint[] memory prices) {
        prices = new uint[](providers_.length);
        
        for(uint32 i = 0; i < providers_.length; i++) {
            prices[i] = providersPrice[ai_method_id_][providers_[i]];
        }    
        return prices;
    }
    
    function getMethods(uint32 from_, uint32 to_) public view returns (AiMethod[] memory methods) {
        methods = new AiMethod[](safeSub(to_, from_) + 1);
        uint32 j = 0;
        for(uint32 i = from_; i <= to_; i++){
            methods[j] = aiMethods[i];
            j++;
        }
        return methods;
    }
    
    function getProviders(uint32 from_, uint32 to_) public view returns (CProvider[] memory providers) {
        providers = new CProvider[](safeSub(to_, from_) + 1);
        uint32 j = 0;
        for(uint32 i = from_; i <= to_; i++){
            if(hostsIndex[i] != address(0)){
                providers[j] = hosts[hostsIndex[i]];    
                j++;
            }
        }
        return providers;
    }
	
	function withdraw() public{
		uint amount = eth[msg.sender];
		eth[msg.sender] = 0;
        msg.sender.transfer(amount);
		emit Withdraw(msg.sender, amount);
	}
	
	/* Oracle */
	/* this function is called by Link s.c.!*/
	function onTokenTransfer(address from, uint amount, bytes memory data) public returns (bool success){
        require(amount == oracleFee, "amount and fee must be ==.");
        require(useOracle, "Use of oracle disabled.");
        bytes memory tmp_addr = new bytes(20);
        uint8 u = 0;
        uint8 i;
        for (i = 0; i < 20; i++){
            tmp_addr[u++] = data[i];
        } 
        address user = bytesToAddress(tmp_addr);
        
        u = 32 - uint8(data.length - 20);
        bytes memory tmp_num = new bytes(32);
        for (i = 20; i < data.length; i++){
            tmp_num[u++] = data[i];
        } 
        uint method_id = sliceUint(tmp_num, 0);

        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        
        string memory url = strConcat(url0, uint2str(method_id), url1, toString(abi.encodePacked(user)));
        request.add("get", url);
        request.add("path", "isAllowed");
        bytes32 request_id = sendChainlinkRequestTo(oracleAddr, request, oracleFee);
        
        rToU[request_id] = RequestIdToUser(user, uint32(method_id));
        emit LogAskOracle(from, amount, data);
        return true;
    }

    /* called by oracle (callback)*/
    function fulfill(bytes32 _requestId, bool _allow) public recordChainlinkFulfillment(_requestId) {
        RequestIdToUser memory tt = rToU[_requestId];
        allowUserToBuy[tt.method_id][tt.user] = _allow;
    }
    
    function isUserAllowed(address _user, uint32 _method_id) public view returns (bool){
		return allowUserToBuy[_method_id][_user];
	}

    function bytesToAddress(bytes memory bys) private pure returns (address addr) {
        assembly {
            addr := mload(add(bys, 20))
        } 
    }
    
    function sliceUint(bytes memory bs, uint start_) private pure returns (uint){
        uint x;
        assembly {
            x := mload(add(bs, add(0x20, start_)))
        }
        return x;
    }
    
    function strConcat(string memory _a, string memory _b, string memory _c, string memory _d) internal pure returns (string memory){
        bytes memory _ba = bytes(_a);
        bytes memory _bb = bytes(_b);
        bytes memory _bc = bytes(_c);
        bytes memory _bd = bytes(_d);
        string memory abcd = new string(_ba.length + _bb.length + _bc.length + _bd.length);
        bytes memory babcd = bytes(abcd);
        uint k = 0;
        uint i = 0;
        for (i = 0; i < _ba.length; i++) babcd[k++] = _ba[i];
        for (i = 0; i < _bb.length; i++) babcd[k++] = _bb[i];
        for (i = 0; i < _bc.length; i++) babcd[k++] = _bc[i];
        for (i = 0; i < _bd.length; i++) babcd[k++] = _bd[i];
        return string(babcd);
    }
	
	function toString(bytes memory data) internal pure returns(string memory) {
        bytes memory alphabet = "0123456789abcdef";
    
        bytes memory str = new bytes(2 + data.length * 2);
        str[0] = "0";
        str[1] = "x";
        for (uint i = 0; i < data.length; i++) {
            str[2+i*2] = alphabet[uint(uint8(data[i] >> 4))];
            str[3+i*2] = alphabet[uint(uint8(data[i] & 0x0f))];
        }
        return string(str);
    }

    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint j = _i;
        uint len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len - 1;
        while (_i != 0) {
            bstr[k--] = byte(uint8(48 + _i % 10));
            _i /= 10;
        }
        return string(bstr);
    }// https://github.com/provable-things/ethereum-api/blob/master/oraclizeAPI_0.5.sol
}