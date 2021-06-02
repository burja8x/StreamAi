import time

from sc2 import *

ef1 = w3.eth.filter({"address": sc.address, "fromBlock": 24000000})

for event in ef1.get_all_entries():
    # print(event)
    topic = Web3.toHex(event["topics"][0])
    if topic not in eee.keys():
        print("ERROR panic ......")
        print(topic)
        continue
    nn = sc.events[eee[topic]]().processReceipt({'logs': [event]})
    print(nn[0]['args'])
    print(nn)
    print(event)

print()

while True:
    time.sleep(5)
    for event in ef1.get_new_entries():
        #print(event)
        topic = Web3.toHex(event["topics"][0])
        if topic not in eee.keys():
            print("ERROR panic ......")
            print(topic)
            print(event)
            continue
        print("NEW Event:", eee[topic])
        nn = sc.events[eee[topic]]().processReceipt({'logs': [event]})
        print(nn[0]['args'])
        # do something with this event.
        # if buyAi
        #       -> run checks
        #       -> run container (but wait 10 block (conformation time ....))
        #       -> new Tx Start. send EC MQTT link
        #       -> ...
        # if new Ai Method (SellAi)
        #       -> run method to see if it works...
        #       -> if it works ... new tx allowAiMethod
        # if Complaint -> report to admin.
        #
        # _______other events are not critical for platform to receive.
        #
        # Client browser side ...
        # watch changes in price (MethodCost, ContainerCost)
        # info --> Complaint
        # if client accepts deal
        #       get info about deal. (BuyAi, Start, End)