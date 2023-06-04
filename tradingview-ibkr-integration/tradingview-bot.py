"""
Routes and views for the flask application.
"""

from datetime import datetime
from typing import List
#from TradingViewInteractiveBrokers import app
from sanic import Sanic
from sanic import response
#import asyncio
#import ast
import nest_asyncio
import datetime
from ib_insync import *


# Create Sanicobject called app.
app = Sanic(__name__)
#app.ctx.ib = None
#app.config.RESPONSE_TIMEOUT = 100 # in secs

@app.before_server_start
async def connect(app,_):
    app.ctx.ib = await IB().connectAsync('127.0.0.1', 7497, clientId=1, timeout=0)

@app.after_server_stop
async def close(app,_):
    app.ctx.ib.disconnect()

# Create root to easily let us know its on/working.
@app.route('/')
async def root(request):
    return response.text('online')

#Check every minute if we need to reconnect to IB
async def checkIfReconnect():
    print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " Checking if we need to reconnect")
    #Reconnect if needed
    if not app.ib.isConnected() or not app.ib.client.isConnected():
        try:
            print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " Reconnecting")
            app.ib.disconnect()
            app.ib = IB()
            app.ib.connect('127.0.0.1', 7497, clientId=1) #7497 paper account 7496 live account
            app.ib.errorEvent += onError
            print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " Reconnect Success")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("Make sure TWS or Gateway is open with the correct port")
            print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " : " + str(e))
    return ''
@app.route('/webhook/crypto', methods=['POST'])
async def webhookCrypto(request):
    print(request)
    if request.method == 'POST':
        #Check if we need to reconnect with IB
        #await checkIfReconnect()
        #with await IB().connectAsync('127.0.0.1', 7497, clientId=2) as ib:

        # Parse the string data from tradingview into a python dict
        data = request.json
        order = MarketOrder("BUY",1,cashQty=50000)
        print(data['symbol'])
        print(data['symbol'][0:3])
        print(data['symbol'][3:6])
        contract = Crypto(data['symbol'][0:3],'PAXOS',data['symbol'][3:6]) #Get first 3 chars BTC then last 3 for currency USD
        #qualifiedContracts: List[Contract] = asyncio.new_event_loop().run_until_complete(app.ib.qualifyContracts(contract))
        contract = await app.ctx.ib.qualifyContractsAsync(contract)
        #app.ib.qualifyContracts(contract)
        #or stock for example 
        #contract = Stock('SPY','SMART','USD')
        print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " Buying: "+ str(data['symbol']))
        trade: Trade = app.ctx.ib.placeOrder(contract[0], order)
        print(trade) 
        # bars = app.ctx.ib.reqHistoricalData(
        #         contract,
        #         endDateTime='',
        #         durationStr='1 D',
        #         barSizeSetting='5 mins',
        #         whatToShow='Trades',
        #         useRTH=False,
        #         formatDate=1
        #         )
        # df = util.df(bars) 
        # print(df)      
    return response.json({"orderStatus": trade.orderStatus.status, "orderId": trade.orderStatus.orderId})
    #return response.json({})

@app.route('/webhook/stock', methods=['POST'])
async def webhookStock(request):
    print(request)
    if request.method == 'POST':
        #Check if we need to reconnect with IB
        #await checkIfReconnect()
        #with await IB().connectAsync('127.0.0.1', 7497, clientId=2) as ib:

        # Parse the string data from tradingview into a python dict
        data = request.json
        order = MarketOrder("BUY",1,account=app.ctx.ib.wrapper.accounts[0], tif="GTC")

        contract = Stock('AAPL','SMART', 'USD') 
        #qualifiedContracts: List[Contract] = asyncio.new_event_loop().run_until_complete(app.ib.qualifyContracts(contract))
        contract = await app.ctx.ib.qualifyContractsAsync(contract)
        #app.ib.qualifyContracts(contract)
        #or stock for example 
        #contract = Stock('SPY','SMART','USD')
        print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " Buying: "+ str(data['symbol']))
        trade: Trade = app.ctx.ib.placeOrder(contract[0], order)
        print(trade) 
        # bars = app.ctx.ib.reqHistoricalData(
        #         contract,
        #         endDateTime='',
        #         durationStr='1 D',
        #         barSizeSetting='5 mins',
        #         whatToShow='Trades',
        #         useRTH=False,
        #         formatDate=1
        #         )
        # df = util.df(bars) 
        # print(df)      
    return response.json({"orderStatus": trade.orderStatus.status, "orderId": trade.orderStatus.orderId})

#On IB Error
def onError(self,reqId, errorCode, errorString, contract):
    print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " : " + str(errorCode))
    print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " : " + str(errorString))
if __name__ == '__main__':
    #IB Connection
    #Connect to IB on init
    #app.ib = IB()
    print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " Connecting to IB")
    #app.ib.connect('127.0.0.1', 7497, clientId=1) #7497 paper account 7496 live account
    print((datetime.datetime.now().strftime("%b %d %H:%M:%S")) + " Successfully Connected to IB")
    #app.ib.errorEvent += onError
    app.run(port=5000)