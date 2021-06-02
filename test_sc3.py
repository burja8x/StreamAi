from unittest import TestCase

from sc2 import *
import random
import time


class Test(TestCase):
    def test_1_admin_c(self):
        a = send_tx(sc.functions.changeFeeAccount(accX0.address), accA)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.changeWaitTime(5, 10), accA)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.changeFeeMake(Web3.toWei(0.00003, 'ether')), accA)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.changeFeeTake(11), accA)  # = 1.1 %
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.changeWaitTime(11, 100010), accA)
        self.assertEqual(a[1], 1)

    def test_2_if_exist_fail(self):
        b = sc.functions.hosts(accP0.address).call()
        c = sc.functions.hosts(accP1.address).call()

        a = send_tx(sc.functions.newCProvider("roža", 100001, 256, 10, 10), accP0)

        #self.assertEqual(a[1], 0 if c[10] == 0 else 1)

        a = send_tx(sc.functions.newCProvider("apple", 100000, 256, 10, 10), accP1)
        #self.assertEqual(a[1], 0 if b[10] == 0 else 1)

        d = sc.functions.hosts(accP1.address).call()
        a = send_tx(sc.functions.newCProvider("ibm", 33358, 256, 20, 10), accP1)
        #self.assertEqual(a[1], 0 if d[10] == 0 else 1)

    def test_3_change_provider_data(self):
        i = random.randint(1000, 1000000)
        j = random.randint(3, 99)
        k = random.randint(3, 99)
        g = random.randint(3, 99)

        a = send_tx(sc.functions.changeCProviderData(i, j, g, k), accP1)
        self.assertEqual(a[1], 1)

        b = sc.functions.hosts(accP1.address).call()
        self.assertEqual(b[2], i)
        self.assertEqual(b[3], j)
        self.assertEqual(b[4], g)
        self.assertEqual(b[5], k)

        a = send_tx(sc.functions.changeCProviderData(1100000, 2000, 30, 200), accP1)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.changeCProviderData(1100000, 2000, 30, 200), accP0)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.changeCProviderData(1100000, 2000, 20, 200), accP2)
        self.assertEqual(a[1], 0)

    def test_4_change_provider_data_1(self):
        with self.assertRaises(Exception):
            a = send_tx(sc.functions.changeCProviderData(10000000000, 10, 1, 10), accP1)

        with self.assertRaises(Exception):
            a = send_tx(sc.functions.changeCProviderData(10000, 100000000, 1, 10), accP1)

        with self.assertRaises(Exception):
            a = send_tx(sc.functions.changeCProviderData(10000, 100, 10, 100000000), accP1)

    def test_5_change_provider_data_2(self):
        a = send_tx(sc.functions.changeCProviderData(1000, 10, 1, 10), accX1)
        self.assertEqual(a[1], 0)

    def test_6_allowCProvider(self):
        a = send_tx(sc.functions.allowCProvider(accP0.address, True), accX1)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.allowCProvider(accP0.address, True), accA)
        self.assertEqual(a[1], 1)
        hc = sc.functions.hostCounter().call() + 1
        # error  ====
        print(hc)
        p = sc.functions.getProviders(1, hc).call()
        id = 0
        for x in p:
            if x[11] == accP0.address:
                id = x[10]
        b = sc.functions.hostsIndex(id).call()
        self.assertEqual(b, accP0.address)

        a = send_tx(sc.functions.allowCProvider(accP0.address, False), accA)
        self.assertEqual(a[1], 1)

        b = sc.functions.hostsIndex(id).call()
        self.assertEqual(b, accP0.address)

        a = send_tx(sc.functions.allowCProvider(accP0.address, True), accA)
        self.assertEqual(a[1], 1)
        b = sc.functions.hostsIndex(id).call()
        self.assertEqual(b, accP0.address)

    def test_7_add_method(self):
        feeMake = Web3.fromWei(sc.functions.feeMake().call(), 'ether')

        a = send_tx(sc.functions.sell("Detekcija mask", 512, 1, False, Web3.toWei(0.00000012, 'ether'),
                                      "bafybeifk6r6ugz62kdrkeitqukase2fojvt6gfasafvzv3rykczww7qawm",
                                      False, "ec dockerHubLink"), accM0,
                    value=feeMake)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.sell("Detekcija mask v2", 1024, 1, True, Web3.toWei(0.00000022, 'ether'),
                                      "bafybeifk6r6ugz62kdrkeitqukase2fojvt6gfasafvzv3rykczww7qawm",
                                      False, "ec dockerHubLink"), accM0,
                    value=feeMake)
        self.assertEqual(a[1], 1)
        #  https://nft.storage/files/
        a = send_tx(sc.functions.sell("vreme", 4096, 4, False, Web3.toWei(0.00000019, 'ether'),
                                      "bafybeifk6r6ugz62kdrkeitqukase2fojvt6gfasafvzv3rykczww7qawm",
                                      False, "ec dockerHubLink"), accM1,
                    value=feeMake)
        self.assertEqual(a[1], 1)

    def test_8_allow_method(self):
        m = sc.functions.methodCounter().call()
        a = send_tx(sc.functions.allowAiMethod(m - 2, True), accA)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.allowAiMethod(m - 1, True), accA)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.allowAiMethod(m, True), accA)
        self.assertEqual(a[1], 1)

    def test_9_set_c_price(self):
        m = sc.functions.methodCounter().call()
        p1 = Web3.toWei(0.000000671, 'ether')
        p2 = Web3.toWei(0.000000682, 'ether')
        a = send_tx(sc.functions.setContainerCost(m - 2, p1), accP0)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.allowCProvider(accP1.address, True), accA)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.setContainerCost(m - 2, p2), accP1)
        self.assertEqual(a[1], 1)
        array = [accP0.address, accP1.address]
        b = sc.functions.getPricesOfProviders(m - 2, array).call()
        self.assertEqual(p1, b[0])
        self.assertEqual(p2, b[1])

        a = send_tx(sc.functions.setContainerCost(m - 2, 0), accP0)
        self.assertEqual(a[1], 1)
        b = sc.functions.getPricesOfProviders(m - 2, array).call()
        self.assertEqual(0, b[0])

        a = send_tx(sc.functions.setContainerCost(m - 1, p1), accP0)
        self.assertEqual(a[1], 1)
        a = send_tx(sc.functions.setContainerCost(m - 2, p1), accP0)
        self.assertEqual(a[1], 1)


class Test_Buy(TestCase):
    def test_1_Buy(self):
        buy_time = 16
        method_id = sc.functions.methodCounter().call() - 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC link video streem..."),
                    accU1, value=end_price)
        self.assertEqual(a[1], 1)

        end_price = Web3.fromWei(m + n + 1000, 'ether')
        a = send_tx(sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC link video streem..."),
                    accU0, value=end_price)
        self.assertEqual(a[1], 1)

        c = sc.functions.dealIdCounter().call()

        l0 = sc.functions.locked(c - 1).call()
        l1 = sc.functions.locked(c).call()
        self.assertEqual(l0[0], l1[0])
        self.assertEqual(l0[2], l1[2])
        self.assertNotEqual(l0[4], l1[4])

        end_price = Web3.fromWei(m + n - 1, 'ether')
        a = send_tx(sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC link video streem..."),
                    accU0, value=end_price)
        self.assertEqual(a[1], 0)

    def test_2_Buy(self):
        buy_time = 21
        method_id = sc.functions.methodCounter().call() - 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC link video streem..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        dealId = sc.functions.dealIdCounter().call()
        b = send_tx(sc.functions.complaint(dealId, "not working !!!"), accU0)
        self.assertEqual(b[1], 0)

        b = send_tx(sc.functions.complaint(dealId, "not workinggdf !!!"), accU1)
        self.assertEqual(b[1], 1)

        b = send_tx(sc.functions.complaint(dealId, "not workihrtng !!!"), accU1)
        self.assertEqual(b[1], 0)

        b = send_tx(sc.functions.complaint(dealId, "not workihrtng !!!"), accU2)
        self.assertEqual(b[1], 0)

    def test_3_Buy(self):
        buy_time = 2
        method_id = sc.functions.methodCounter().call() - 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC link video streem..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)  # time to small....

    def test_4_Buy_Start_Stop(self):
        buy_time = 20
        method_id = sc.functions.methodCounter().call() - 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        dealId = sc.functions.dealIdCounter().call()
        a = send_tx(sc.functions.start(dealId, "THIS is EC(# mqtt link)"), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.delivered(dealId, False), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.delivered(dealId, False), accA)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.start(dealId, "THIS is EC(# mqtt link)"), accA)
        self.assertEqual(a[1], 0)

    def test_5_Buy_Start_Stop(self):
        buy_time = 20
        method_id = 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        dealId = sc.functions.dealIdCounter().call()
        a = send_tx(sc.functions.start(dealId, "THIS is EC(# mqtt link)"), accU1)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.delivered(dealId, False), accU1)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.start(dealId, "THIS is EC(# mqtt link)"), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.delivered(dealId, False), accU0)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.delivered(dealId, False), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.delivered(dealId, False), accA)
        self.assertEqual(a[1], 0)

    def test_6_Buy_Disable(self):
        buy_time = 19
        method_id = sc.functions.methodCounter().call() - 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.allowAiMethod(method_id, False), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.allowAiMethod(method_id, True), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .h7uz789678967....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

    def test_7_Buy_Disable_P(self):
        buy_time = 19
        method_id = sc.functions.methodCounter().call() - 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.allowCProvider(accP0.address, False), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.allowCProvider(accP0.address, True), accA)
        self.assertEqual(a[1], 1)

    def test_8_Buy_Disable_Acctive(self):
        buy_time = 19
        method_id = sc.functions.methodCounter().call() - 2
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        methodX = sc.functions.aiMethods(method_id).call()
        if methodX[0] == accM0.address:
            acc = accM0
        elif methodX[0] == accM1.address:
            acc = accM1
        elif methodX[0] == accM2.address:
            acc = accM2
        else:
            self.assertTrue(False)

        a = send_tx(sc.functions.activateAiMethod(method_id, False), acc)
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU0, value=end_price)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.activateAiMethod(method_id, True), acc)
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU2, value=end_price)
        self.assertEqual(a[1], 1)

    def test_9_Buy_Ram_Cpus(self):
        buy_time = 19
        method_id = 1
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        p0 = sc.functions.hosts(accP0.address).call()
        print("maxram", p0[2], "maxCpus", p0[3], "maxGpus", p0[4], "maxInst", p0[5])
        print("usedRam", p0[6], "usedCpus", p0[7], "usedGpus", p0[8], "usedInst", p0[9])

        a = send_tx(sc.functions.changeCProviderData(p0[6] + 50, p0[3], p0[4], p0[5]), accP0)  # ram
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.changeCProviderData(p0[6], p0[7], p0[4], p0[9]), accP0)  # gpu
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.changeCProviderData(p0[2], p0[7], p0[4], p0[5]), accP0)  # cpus
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.changeCProviderData(p0[2], p0[3], p0[4], p0[9]), accP0)  # cpus
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)

        a = send_tx(sc.functions.changeCProviderData(p0[2], p0[3], p0[4], p0[9] + 1), accP0)  # inst
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        a = send_tx(sc.functions.changeCProviderData(p0[2], p0[3], p0[4], p0[5]), accP0)
        self.assertEqual(a[1], 1)

        p0 = sc.functions.hosts(accP0.address).call()
        print("maxram", p0[2], "maxCpus", p0[3], "maxGpus", p0[4], "maxInst", p0[5])
        print("usedRam", p0[6], "usedCpus", p0[7], "usedGpus", p0[8], "usedInst", p0[9])


class Test_Buy_X(TestCase):
    def test_1_delivered(self):
        k_state = 0
        for dealId in range(1, sc.functions.dealIdCounter().call()):
            ll = sc.functions.locked(dealId).call()
            print("locked:", ll)
            if ll[0] != 0:
                eth_provider = sc.functions.eth(ll[1]).call()
                eth_m_creator = sc.functions.eth(ll[3]).call()
                eth_fee = sc.functions.eth(sc.functions.feeAccount().call()).call()
                eth_buyer = sc.functions.eth(ll[6]).call()
                if k_state == 0:
                    print("delivered without error")
                    print(eth_provider, eth_m_creator, eth_fee, eth_buyer)

                    a = send_tx(sc.functions.delivered(dealId, False), accA)
                    self.assertEqual(a[1], 1)
                    ttt = sc.functions.locked(dealId).call()
                    self.assertEqual(ttt[0], 0)
                    self.assertEqual(ttt[2], 0)
                    self.assertEqual(ttt[4], 0)

                    self.assertEqual(eth_buyer, sc.functions.eth(ll[6]).call())
                    self.assertEqual(eth_provider + ll[0], sc.functions.eth(ll[1]).call())
                    self.assertEqual(eth_m_creator + ll[2], sc.functions.eth(ll[3]).call())
                    self.assertEqual(eth_fee + ll[4], sc.functions.eth(sc.functions.feeAccount().call()).call())

                    k_state = 1
                elif k_state == 1:
                    print("delivered with error")
                    print(eth_provider, eth_m_creator, eth_fee, eth_buyer)

                    a = send_tx(sc.functions.delivered(dealId, True), accA)
                    self.assertEqual(a[1], 1)
                    ttt = sc.functions.locked(dealId).call()
                    self.assertEqual(ttt[0], 0)
                    self.assertEqual(ttt[2], 0)
                    self.assertEqual(ttt[4], 0)

                    self.assertEqual(eth_buyer + ll[0] + ll[2] + ll[4], sc.functions.eth(ll[6]).call())
                    self.assertEqual(eth_provider, sc.functions.eth(ll[1]).call())
                    self.assertEqual(eth_m_creator, sc.functions.eth(ll[3]).call())
                    self.assertEqual(eth_fee, sc.functions.eth(sc.functions.feeAccount().call()).call())

                    k_state = 0
        print("end")
        # pazi da ni user == drugim (admin , ....)


        # for i in allAcc.keys():
        #     print(i, allAcc[i].address, Web3.fromWei(sc.functions.eth(allAcc[i].address).call(), 'ether'))

    def test_4_SAFU_user(self):
        # get first working method....
        method_id = -1
        pprice = -1
        provider_a = ""
        p = sc.functions.getProviders(1, sc.functions.hostCounter().call() + 1).call()
        arrayProviders = []
        for ww in p:
            if ww[1]:
                arrayProviders.append(ww[11])
        n = sc.functions.methodCounter().call()
        m = sc.functions.getMethods(1, n + 1).call()
        y = 0
        for x in m:
            if not x[9] and x[6] and x[7]:
                print(x)
                gg = 0
                for pp in sc.functions.getPricesOfProviders(1+y, arrayProviders).call():

                    if pp != 0:
                        print(pp)
                        method_id = y+1
                        pprice = pp
                        provider_a = arrayProviders[gg]
                    gg += 1
            y += 1

        self.assertNotEqual(method_id, -1)
        self.assertNotEqual(pprice, -1)
        self.assertNotEqual(provider_a, "")
        #

        buy_time = 19
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()

        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')
        print(end_price)

        a = send_tx(sc.functions.changeWaitTime(500, 500), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, provider_a, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        dealId = sc.functions.dealIdCounter().call()

        ll = sc.functions.locked(dealId).call()
        print("release Block ", ll[5], "   l ", w3.eth.block_number)
        # eth_provider = sc.functions.eth(ll[1]).call()
        # eth_m_creator = sc.functions.eth(ll[3]).call()
        # eth_fee = sc.functions.eth(sc.functions.feeAccount().call()).call()
        # eth_buyer = sc.functions.eth(ll[6]).call()

        time.sleep(30)

        a = send_tx(sc.functions.returnToBuyerSAFU(dealId), accU1)
        self.assertEqual(a[1], 0)
        #
        #----------------------------------------------------------------------------
        a = send_tx(sc.functions.changeWaitTime(0, 0), accA)
        self.assertEqual(a[1], 1)

        a = send_tx(
            sc.functions.buy(method_id, provider_a, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 1)

        dealId = sc.functions.dealIdCounter().call()

        ll = sc.functions.locked(dealId).call()
        print("release Block ", ll[5], "   l ", w3.eth.block_number)
        time.sleep(30)

        a = send_tx(sc.functions.returnToBuyerSAFU(dealId), accU1)
        self.assertEqual(a[1], 1)



    def test_2_Withdraw(self):
        pass

    def test_3_BlockNumber(self):
        pass



    def test_5_change_AskUrl(self):
        print(sc.functions.url0().call())
        print(sc.functions.url1().call())

        url0 = "debela mis .com ...//"
        url1 = "slon je lacen"

        a = send_tx(sc.functions.changeAskUrl(url0, url1), accA)
        self.assertEqual(a[1], 1)

        u0 = sc.functions.url0().call()
        u1 = sc.functions.url1().call()
        print(u0, u1)
        self.assertEqual(u0, url0)
        self.assertEqual(u1, url1)

        a = send_tx(sc.functions.changeAskUrl(
            "https://stream-ai-api.aleksvujic.fun/api/v1/account/isAiMethodAllowedForUser?aiMethodId=",
            "&userEthAddress="), accA)
        self.assertEqual(a[1], 1)

    def test_6_change_Oracle(self):
        # https://market.link/search/jobs?network=42&page=1&search=get%20bool
        print(sc.functions.oracleAddr().call())
        print(sc.functions.jobId().call())
        # print(Web3.toBytes(hexstr="1bc99b4b57034ae4bcc3a6b6f6daaede"))
        # print(Web3.toBytes(text="1bc99b4b57034ae4bcc3a6b6f6daaede"))

        # a = send_tx(sc.functions.changeOracle("0x1b666ad0d20bC4F35f218120d7ed1e2df60627cC", 100000000000000000,
        #                                       Web3.toBytes(text="1bc99b4b57034ae4bcc3a6b6f6daaede")), accA)
        a = send_tx(sc.functions.changeOracle("0x56dd6586DB0D08c6Ce7B2f2805af28616E082455", 100000000000000000,
                                              Web3.toBytes(text="1b2658f2d679437cb2d8db115c646d02")), accA)
        self.assertEqual(a[1], 1)

        print(sc.functions.oracleAddr().call())
        print(sc.functions.jobId().call())

class Test_Buy_Oracle(TestCase):
    mmm_id = 0

    def test_1_not_allowed(self):
        feeMake = Web3.fromWei(sc.functions.feeMake().call(), 'ether')

        a = send_tx(sc.functions.sell("Mask detection", 512, 1, True, Web3.toWei(0.00000013, 'ether'),
                                      "bafybeifk6r6ugz62kdrkeitqukase2fojvt6gfasafvzv3rykczww7qawm",
                                      True, "ec dockerHubLink"), accM0, value=feeMake)
        self.assertEqual(a[1], 1)

        method_id = sc.functions.methodCounter().call()
        a = send_tx(sc.functions.allowAiMethod(method_id, True), accA)
        self.assertEqual(a[1], 1)

        buy_time = 19
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accU1, value=end_price)
        self.assertEqual(a[1], 0)

    def test_2_allowed(self):
        method_id = sc.functions.methodCounter().call()
        m = sc.functions.aiMethods(method_id).call()

        self.assertTrue(m[9])  # if onlyAllowedUsers

        b = sc.functions.isUserAllowed(accX0.address, method_id).call()
        print(b)

        a = send_tx(sc.functions.allowUserToUseMethod(method_id, accX0.address, True), accA)
        self.assertEqual(a[1], 1)

        b = sc.functions.isUserAllowed(accX0.address, method_id).call()
        print(accX0.address, b)
        self.assertEqual(b, True)

        b = sc.functions.isUserAllowed(accU1.address, method_id).call()
        self.assertEqual(b, False)

        a = send_tx(sc.functions.setContainerCost(method_id, 10000000000), accP0)
        buy_time = 18
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        print("provider Price:", pprice)
        print("method Price:", mprice[5])
        print("feeTake:", feeTake)
        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accX0, value=end_price)
        self.assertEqual(a[1], 1)

    def test_3_allowed_false(self):
        method_id = sc.functions.methodCounter().call()
        m = sc.functions.aiMethods(method_id).call()
        print(m)
        self.assertTrue(m[9])  # if onlyAllowedUsers

        a = send_tx(sc.functions.allowUserToUseMethod(method_id, accX0.address, False), accA)
        self.assertEqual(a[1], 1)

        b = sc.functions.isUserAllowed(accX0.address, method_id).call()
        print(b)
        self.assertEqual(b, False)

        buy_time = 23
        pprice = sc.functions.getProviderPrice(method_id, accP0.address).call()
        mprice = sc.functions.aiMethods(method_id).call()
        feeTake = sc.functions.feeTake().call()
        n = (pprice * buy_time) + (mprice[5] * buy_time)
        m = (n * feeTake) / 1000
        end_price = Web3.fromWei(m + n, 'ether')

        a = send_tx(
            sc.functions.buy(method_id, accP0.address, pprice, mprice[5], buy_time, "EC .....m..."),
            accX0, value=end_price)
        self.assertEqual(a[1], 0)

    def test_4_call_link(self):
        method_id = sc.functions.methodCounter().call()
        m = sc.functions.aiMethods(method_id).call()

        self.assertTrue(m[9])  # if onlyAllowedUsers

        b = sc.functions.isUserAllowed(accX1.address, method_id).call()
        if b:
            a = send_tx(sc.functions.allowUserToUseMethod(method_id, accX1.address, False), accA)
            self.assertEqual(a[1], 1)

        b = sc.functions.isUserAllowed(accX1.address, method_id).call()
        self.assertEqual(b, False)

        a = send_tx(sc.functions.changeUserChecker(True), accA)
        self.assertEqual(a[1], 1)

        print(accX1.address, b)

        a = send_tx(scLink.functions.transferAndCall(sc.address, 100000000000000000, Web3.toBytes(
            hexstr=accX1.address[2:]) + Web3.toBytes(method_id)), accX0)
        self.assertEqual(a[1], 1)

        c = 0
        while True:
            b = sc.functions.isUserAllowed(accX1.address, method_id).call()
            print(b)
            if b:
                print(b)
                break

            time.sleep(7)
            if c >= 20:
                self.assertTrue(False)
            c += 1

        b = sc.functions.isUserAllowed(accX1.address, method_id).call()
        print(b)

    def test_5_call_link(self):
        method_id = sc.functions.methodCounter().call()
        m = sc.functions.aiMethods(method_id).call()

        self.assertTrue(m[9])  # if onlyAllowedUsers

        b = sc.functions.isUserAllowed(accX0.address, method_id).call()
        if not b:
            a = send_tx(sc.functions.allowUserToUseMethod(method_id, accX0.address, True), accA)
            self.assertEqual(a[1], 1)

        b = sc.functions.isUserAllowed(accX0.address, method_id).call()
        print(accX0.address, b)
        self.assertEqual(b, True)

        print(accX0.address[2:])
        print(Web3.toBytes(hexstr=accX0.address[2:]) + Web3.toBytes(method_id))

        a = send_tx(scLink.functions.transferAndCall(sc.address, 100000000000000000, Web3.toBytes(
            hexstr=accX0.address[2:]) + Web3.toBytes(method_id)), accX0)
        self.assertEqual(a[1], 1)

        c = 0
        while True:
            b = sc.functions.isUserAllowed(accX0.address, method_id).call()
            print(b)
            if not b:
                print(b)
                break

            time.sleep(7)
            if c >= 20:
                self.assertTrue(False)
            c += 1

        b = sc.functions.isUserAllowed(accX0.address, method_id).call()
        print(b)