from web3 import Web3, HTTPProvider, eth
from time import sleep
import json

w3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/>>>>insert infura key<<<<"))
# https://faucet.kovan.network/


from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

print(w3.isConnected())

# you can create accounts like this.
# for i in range(6):
#     acc0 = w3.eth.account.create("")
#     print(acc0.privateKey)

allAcc = {}

# INSERT your private keys!!!!!
accA = w3.eth.account.privateKeyToAccount(b'')
allAcc["accA"] = accA

accM0 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accM0"] = accM0
accM1 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accM1"] = accM1
accM2 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accM2"] = accM2

accP0 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accP0"] = accP0
accP1 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accP1"] = accP1
accP2 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accP2"] = accP2

accU0 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accU0"] = accU0
accU1 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accU1"] = accU1
accU2 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accU2"] = accU2

accX0 = w3.eth.account.privateKeyToAccount(b"")
allAcc["accX0"] = accX0
accX1 = w3.eth.account.privateKeyToAccount(b'')
allAcc["accX1"] = accX1

# for i in allAcc.keys():
#     print(i, allAcc[i].address, Web3.fromWei(w3.eth.get_balance(allAcc[i].address), 'ether'))


mySC = "0xdfe5606599867509b67f9f716abbcbbe4e863cb9"  # <<--- INSERT SMART CONTRACT ADDRESS

scAddr = Web3.toChecksumAddress(mySC)
# CHANGE ABI IF NEEDED
abi = '[{"inputs":[{"internalType":"uint32","name":"ai_method_id_","type":"uint32"},{"internalType":"bool","name":"activate_","type":"bool"}],"name":"activateAiMethod","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"ai_method_id_","type":"uint32"},{"internalType":"bool","name":"allow_","type":"bool"}],"name":"allowAiMethod","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"provider_","type":"address"},{"internalType":"bool","name":"allow_","type":"bool"}],"name":"allowCProvider","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"method_id_","type":"uint32"},{"internalType":"address","name":"user_","type":"address"},{"internalType":"bool","name":"allow_","type":"bool"}],"name":"allowUserToUseMethod","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"ai_method_id_","type":"uint32"},{"internalType":"address","name":"provider_","type":"address"},{"internalType":"uint256","name":"container_price_","type":"uint256"},{"internalType":"uint256","name":"ai_method_price_","type":"uint256"},{"internalType":"uint24","name":"timeInSec_","type":"uint24"},{"internalType":"string","name":"videoStreamUrl_","type":"string"}],"name":"buy","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"admin_","type":"address"}],"name":"changeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userBuying","type":"address"},{"indexed":false,"internalType":"uint32","name":"aiMethodId","type":"uint32"},{"indexed":false,"internalType":"address","name":"provider","type":"address"},{"indexed":false,"internalType":"uint256","name":"containerPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"aiMethodPrice","type":"uint256"},{"indexed":false,"internalType":"uint24","name":"timeInSec","type":"uint24"},{"indexed":false,"internalType":"uint32","name":"dealId","type":"uint32"},{"indexed":false,"internalType":"string","name":"videoStreamUrl","type":"string"}],"name":"BuyAi","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkCancelled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkFulfilled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"id","type":"bytes32"}],"name":"ChainlinkRequested","type":"event"},{"inputs":[{"internalType":"uint32","name":"ai_method_id_","type":"uint32"},{"internalType":"uint256","name":"price_","type":"uint256"}],"name":"changeAiMethodPrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"url0_","type":"string"},{"internalType":"string","name":"url1_","type":"string"}],"name":"changeAskUrl","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"maxRam_","type":"uint32"},{"internalType":"uint24","name":"maxCpus_","type":"uint24"},{"internalType":"uint24","name":"maxGpus_","type":"uint24"},{"internalType":"uint24","name":"maxRunning_","type":"uint24"}],"name":"changeCProviderData","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"feeAccount_","type":"address"}],"name":"changeFeeAccount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"feeMake_","type":"uint256"}],"name":"changeFeeMake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"feeTake_","type":"uint16"}],"name":"changeFeeTake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"oracleAddr_","type":"address"},{"internalType":"uint256","name":"oracleFee_","type":"uint256"},{"internalType":"bytes32","name":"jobId_","type":"bytes32"}],"name":"changeOracle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"useOracle_","type":"bool"}],"name":"changeUserChecker","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"waitNumberOfBlocksBeforeStart_","type":"uint32"},{"internalType":"uint32","name":"waitNumberOfBlocksAfterStart_","type":"uint32"}],"name":"changeWaitTime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"dealId_","type":"uint32"},{"internalType":"string","name":"text_","type":"string"}],"name":"complaint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"dealId","type":"uint32"},{"indexed":false,"internalType":"string","name":"text","type":"string"}],"name":"Complaint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"aiMethodId","type":"uint32"},{"indexed":false,"internalType":"address","name":"provider","type":"address"},{"indexed":false,"internalType":"uint256","name":"containerCost","type":"uint256"}],"name":"ContainerCost","type":"event"},{"inputs":[{"internalType":"uint32","name":"dealId_","type":"uint32"},{"internalType":"bool","name":"error_","type":"bool"}],"name":"delivered","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"dealId","type":"uint32"},{"indexed":false,"internalType":"bool","name":"error","type":"bool"}],"name":"End","type":"event"},{"inputs":[{"internalType":"bytes32","name":"_requestId","type":"bytes32"},{"internalType":"bool","name":"_allow","type":"bool"}],"name":"fulfill","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"fromUser","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"LogAskOracle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"aiMethodId","type":"uint32"},{"indexed":false,"internalType":"uint256","name":"methodCost","type":"uint256"}],"name":"MethodCost","type":"event"},{"inputs":[{"internalType":"string","name":"name_","type":"string"},{"internalType":"uint32","name":"maxRam_","type":"uint32"},{"internalType":"uint24","name":"maxCpus_","type":"uint24"},{"internalType":"uint24","name":"maxGpus_","type":"uint24"},{"internalType":"uint24","name":"maxRunning_","type":"uint24"}],"name":"newCProvider","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"onTokenTransfer","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"dealId_","type":"uint32"}],"name":"returnToBuyerSAFU","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"name_","type":"string"},{"internalType":"uint32","name":"ram_","type":"uint32"},{"internalType":"uint24","name":"cpus_","type":"uint24"},{"internalType":"bool","name":"gpu_","type":"bool"},{"internalType":"uint256","name":"price_","type":"uint256"},{"internalType":"string","name":"ipfsCID_","type":"string"},{"internalType":"bool","name":"onlyAllowedUsers_","type":"bool"},{"internalType":"string","name":"dockerHubLink_","type":"string"}],"name":"sell","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"payable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userSelling","type":"address"},{"indexed":false,"internalType":"string","name":"name","type":"string"},{"indexed":false,"internalType":"uint32","name":"aiMethodId","type":"uint32"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"uint32","name":"ram","type":"uint32"},{"indexed":false,"internalType":"uint24","name":"cpus","type":"uint24"},{"indexed":false,"internalType":"bool","name":"gpu","type":"bool"},{"indexed":false,"internalType":"string","name":"ipfsCID","type":"string"},{"indexed":false,"internalType":"bool","name":"onlyAllowedUsers","type":"bool"},{"indexed":false,"internalType":"string","name":"dockerHubLink","type":"string"}],"name":"SellAi","type":"event"},{"inputs":[{"internalType":"uint32","name":"ai_method_id_","type":"uint32"},{"internalType":"uint256","name":"containerCost_","type":"uint256"}],"name":"setContainerCost","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"dealId_","type":"uint32"},{"internalType":"string","name":"ECmqttLink_","type":"string"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint32","name":"dealId","type":"uint32"},{"indexed":false,"internalType":"string","name":"ECmqttLink","type":"string"}],"name":"Start","type":"event"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"}],"name":"aiMethods","outputs":[{"internalType":"address","name":"creator","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint32","name":"ram","type":"uint32"},{"internalType":"uint24","name":"cpu","type":"uint24"},{"internalType":"bool","name":"gpuRequired","type":"bool"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bool","name":"Allowed","type":"bool"},{"internalType":"bool","name":"Active","type":"bool"},{"internalType":"string","name":"ipfsCID","type":"string"},{"internalType":"bool","name":"onlyAllowedUsers","type":"bool"},{"internalType":"uint32","name":"id","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"dealIdCounter","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"eth","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeAccount","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeMake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeTake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"from_","type":"uint32"},{"internalType":"uint32","name":"to_","type":"uint32"}],"name":"getMethods","outputs":[{"components":[{"internalType":"address","name":"creator","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint32","name":"ram","type":"uint32"},{"internalType":"uint24","name":"cpu","type":"uint24"},{"internalType":"bool","name":"gpuRequired","type":"bool"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"bool","name":"Allowed","type":"bool"},{"internalType":"bool","name":"Active","type":"bool"},{"internalType":"string","name":"ipfsCID","type":"string"},{"internalType":"bool","name":"onlyAllowedUsers","type":"bool"},{"internalType":"uint32","name":"id","type":"uint32"}],"internalType":"struct AiPlatforma.AiMethod[]","name":"methods","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"ai_method_id_","type":"uint32"},{"internalType":"address[]","name":"providers_","type":"address[]"}],"name":"getPricesOfProviders","outputs":[{"internalType":"uint256[]","name":"prices","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"ai_method_id_","type":"uint32"},{"internalType":"address","name":"provider_","type":"address"}],"name":"getProviderPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"from_","type":"uint32"},{"internalType":"uint32","name":"to_","type":"uint32"}],"name":"getProviders","outputs":[{"components":[{"internalType":"string","name":"name","type":"string"},{"internalType":"bool","name":"Allowed","type":"bool"},{"internalType":"uint32","name":"maxRam","type":"uint32"},{"internalType":"uint24","name":"maxCpus","type":"uint24"},{"internalType":"uint24","name":"maxGpus","type":"uint24"},{"internalType":"uint24","name":"maxRunning","type":"uint24"},{"internalType":"uint32","name":"usedRam","type":"uint32"},{"internalType":"uint24","name":"usedCpus","type":"uint24"},{"internalType":"uint24","name":"usedGpus","type":"uint24"},{"internalType":"uint24","name":"usedInstances","type":"uint24"},{"internalType":"uint32","name":"id","type":"uint32"},{"internalType":"address","name":"addr","type":"address"}],"internalType":"struct AiPlatforma.CProvider[]","name":"providers","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"hostCounter","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"hosts","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"bool","name":"Allowed","type":"bool"},{"internalType":"uint32","name":"maxRam","type":"uint32"},{"internalType":"uint24","name":"maxCpus","type":"uint24"},{"internalType":"uint24","name":"maxGpus","type":"uint24"},{"internalType":"uint24","name":"maxRunning","type":"uint24"},{"internalType":"uint32","name":"usedRam","type":"uint32"},{"internalType":"uint24","name":"usedCpus","type":"uint24"},{"internalType":"uint24","name":"usedGpus","type":"uint24"},{"internalType":"uint24","name":"usedInstances","type":"uint24"},{"internalType":"uint32","name":"id","type":"uint32"},{"internalType":"address","name":"addr","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"}],"name":"hostsIndex","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"},{"internalType":"uint32","name":"_method_id","type":"uint32"}],"name":"isUserAllowed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"jobId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"}],"name":"locked","outputs":[{"internalType":"uint256","name":"ethProvider","type":"uint256"},{"internalType":"address","name":"provider","type":"address"},{"internalType":"uint256","name":"ethAiCreator","type":"uint256"},{"internalType":"address","name":"aiCreator","type":"address"},{"internalType":"uint256","name":"ethFee","type":"uint256"},{"internalType":"uint32","name":"releaseBlock","type":"uint32"},{"internalType":"address","name":"buyer","type":"address"},{"internalType":"uint32","name":"timeInSec","type":"uint32"},{"internalType":"uint32","name":"methodId","type":"uint32"},{"internalType":"bool","name":"complaintWritten","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxTime","outputs":[{"internalType":"uint24","name":"","type":"uint24"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"methodCounter","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minTime","outputs":[{"internalType":"uint24","name":"","type":"uint24"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"oracleAddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"oracleFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"rToU","outputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint32","name":"method_id","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"url0","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"url1","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"useOracle","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"waitNumberOfBlocksAfterStart","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"waitNumberOfBlocksBeforeStart","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"}]'
abi = json.loads(abi)
sc = w3.eth.contract(address=scAddr, abi=abi)

# LINK SMART CONTRACT ADDRESS + LINK ABI 
scLinkAddr = Web3.toChecksumAddress("0xa36085f69e2889c224210f603d836748e7dc0088")
linkAbi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"transferAndCall","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"}]'
linkAbi = json.loads(linkAbi)
scLink = w3.eth.contract(address=scLinkAddr, abi=linkAbi)
#

# for i in allAcc.keys():
#     print(i, allAcc[i].address, Web3.fromWei(sc.functions.eth(allAcc[i].address).call(), 'ether'))

fBlock = 24267760
efBuyAi = sc.events.BuyAi.createFilter(fromBlock=fBlock)
efWithdraw = sc.events.Withdraw.createFilter(fromBlock=fBlock)
efSellAi = sc.events.SellAi.createFilter(fromBlock=fBlock)
efStart = sc.events.Start.createFilter(fromBlock=fBlock)
efEnd = sc.events.End.createFilter(fromBlock=fBlock)
efComplaint = sc.events.Complaint.createFilter(fromBlock=fBlock)
efContainerCost = sc.events.ContainerCost.createFilter(fromBlock=fBlock)
efMethodCost = sc.events.MethodCost.createFilter(fromBlock=fBlock)

eee = {efBuyAi.filter_params["topics"][0]: 'BuyAi', efWithdraw.filter_params["topics"][0]: 'Withdraw',
          efSellAi.filter_params["topics"][0]: 'SellAi', efStart.filter_params["topics"][0]: 'Start',
          efEnd.filter_params["topics"][0]: 'End', efComplaint.filter_params["topics"][0]: 'Complaint',
          efContainerCost.filter_params["topics"][0]: 'ContainerCost',
          efMethodCost.filter_params["topics"][0]: 'MethodCost'}


# print("FeeTake:", sc.functions.feeTake().call())
# print("FeeMake:", sc.functions.feeMake().call())
# print("MaxTime:", sc.functions.maxTime().call())
# print("MinTime:", sc.functions.minTime().call())
# print("wait before start:", sc.functions.waitNumberOfBlocksBeforeStart().call())
# print("wait after start:", sc.functions.waitNumberOfBlocksAfterStart().call())
#
# print("Admin:", sc.functions.admin().call())
# print("FeeAccount:", sc.functions.feeAccount().call())
# print("locked:", sc.functions.locked(0).call())
# print("hosts:", sc.functions.hosts(accP0.address).call())
# print("eth:", sc.functions.eth(accA.address).call())
# print("Mathods:", sc.functions.AiMethods(0).call())
# print("providersPrice:", sc.functions.getProviderPrice(0, accP0.address).call())
#
# print("methodCounter:", sc.functions.methodCounter().call())
# print("dealIdCounter:", sc.functions.dealIdCounter().call())

# print("hostCounter:", sc.functions.hostCounter().call())


# print("getProviders:", sc.function.getProviders(0, sc.functions.hostCounter().call()))

# print("getPricesOfProviders:", sc.functions.getPricesOfProviders(0, [accP0.address, accP1.address, accP2.address]).call())

# print("getMethods:", sc.function.getMethods(0, sc.functions.methodCounter().call()).call())




def send_eth(to, amount, acc):
    signed_txn = w3.eth.account.sign_transaction(dict(
        nonce=w3.eth.get_transaction_count(acc.address),
        gasPrice=w3.eth.gas_price,
        gas=21000,
        to=to,
        value=Web3.toWei(amount, 'ether'),
        data=b'',
        ),
        acc.privateKey)
    tx = Web3.toHex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))
    receipt = w3.eth.waitForTransactionReceipt(tx)
    print(receipt)
    print("Status:", receipt.status)
    return tx

def send_tx(tran, acc, value=0, printEvent=False):
    tr = tran.buildTransaction(
        {'chainId': w3.eth.chain_id, 'gas': 300000, 'nonce': w3.eth.get_transaction_count(acc.address), 'value': Web3.toWei(value, 'ether')})
    try:
        ss = w3.eth.estimate_gas(tran.buildTransaction({'from': acc.address}))
        tr['gas'] = ss
    except:
        print("Warning in estimate_gas")
    #print(tr)
    signed_tx = w3.eth.account.sign_transaction(tr, acc.key)
    tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    receipt = w3.eth.wait_for_transaction_receipt(tx)
    sleep(1)

    if receipt.status != 1:
        print(tran.fn_name, "Status:", receipt.status, "https://kovan.etherscan.io/tx/" + Web3.toHex(tx))
    else:
        print(tran.fn_name, "Status:", receipt.status)

    dic_event = ""
    if printEvent:
        topic = Web3.toHex(receipt["logs"][0]["topics"][0])
        if topic not in eee.keys():
            print("ERROR panic ......")
            print(topic)
            print(receipt)
        else:
            nn = sc.events[eee[topic]]().processReceipt(receipt)
            dic_event = nn[0]['args']
            print(dic_event)

    return tx, receipt.status, receipt, tr, dic_event





