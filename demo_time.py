from sc2 import *
import time


p_count = sc.functions.hostCounter().call()
print("getProviders", p_count)
print(p_count)
p = sc.functions.getProviders(1, p_count).call()
for x in p:
    print(x)
print()
# ---------------------------------
method_counter = sc.functions.methodCounter().call()
print("\ngetMethods", method_counter)
m = sc.functions.getMethods(0, method_counter).call()
for x in m:
    print(x)
print()

array_providers = [x[11] for x in p if x[1]]


print("getPricesOfProviders")
for i in range(1, method_counter+1):
    cost = sc.functions.getPricesOfProviders(i, array_providers).call()
    print("AiMethod:", i, cost, "     ->     ", [Web3.fromWei(p, 'ether') for p in cost])

method_id = 4
# send_tx(sc.functions.allowUserToUseMethod(method_id, accX1.address, False), accA)
# send_tx(sc.functions.setContainerCost(method_id, 112300000000), accP1)


# b = sc.functions.isUserAllowed(accX1.address, method_id).call()
# print("is", accX1.address, "allowed to use method 4 ? ", b)
#
#
# a = send_tx(scLink.functions.transferAndCall(mySC, 100000000000000000, Web3.toBytes(
#             hexstr=accX1.address[2:]) + Web3.toBytes(method_id)), accX0)
#
# c = 0
# while True:
#     b = sc.functions.isUserAllowed(accX1.address, method_id).call()
#     print(b)
#     if b:
#         print(accX1.address, "is allowed to call Buy function")
#         break
#
#     time.sleep(3)
#
#     if c >= 30:
#         print("no response from oracle..!!!!!")
#         exit()
#     c += 1


#
buy_time = 18
pprice = sc.functions.getProviderPrice(method_id, accP1.address).call()
mprice = sc.functions.aiMethods(method_id).call()
feeTake = sc.functions.feeTake().call()
n = (pprice * buy_time) + (mprice[5] * buy_time)
m = (n * feeTake) / 1000
end_price = Web3.fromWei(m + n, 'ether')
print("provider Price:", pprice)
print("method Price:", mprice[5])
print("feeTake:", feeTake)

a = send_tx(
    sc.functions.buy(method_id, accP1.address, pprice, mprice[5], buy_time, "EC ..video stream url.....m..."),
    accX1, value=end_price)