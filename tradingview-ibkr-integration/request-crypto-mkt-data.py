from ib_insync import *

try:
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    contract = Crypto('BTC','PAXOS', 'USD')
    ib.qualifyContracts(contract)
    data = ib.reqMktData(contract)
    print(str(data))
    price = data.marketPrice()
    print(str(price))
except Exception as e:
    print(str(e))