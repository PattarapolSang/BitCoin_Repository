from operator import imod
import websocket, json, pprint
import talib
import numpy as np

from binance.client import Client
from binance.enums import *

RSI_PEROID = 14             # RSI 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "BNBBUSD"
TRADE_QUANTITY = 0.02
#TRADE_QUANTITY_SELL = 0.02

import config

print('This is API_KEY: {}'.format(config.API_KEY))
print('This is API_SECRET: {}'.format(config.API_SECRET))

client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity,symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order")
        #order = client.create_order(symbol=symbols, side=sides, type=order_type, quantity=quantitys)
        orderss = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(orderss)
        print('Order complete')
    except Exception as e:
        print('Something wrong')
        return False
    
    return True

balance_BNB  = client.get_asset_balance(asset='BNB')
balance_BUSD = client.get_asset_balance(asset='BUSD')
print(balance_BUSD)

#order_succeeded_buy = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
order_succeeded_sell = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
#order_buy = client.order_market_buy(symbol=TRADE_SYMBOL, quantity=TRADE_QUANTITY)
#order_sell  = client.order_market_sell(symbol=TRADE_SYMBOL, quantity=TRADE_QUANTITY)

print('Finish Order!!!!!!')

info = client.get_account()
balance = client.get_asset_balance(asset='BUSD')
status = client.get_account_status()
status_API = client.get_account_api_trading_status()

orders = client.get_open_orders(symbol='BNBBUSD')

#print(info)
print(balance)
print(status)
print(status_API)

print(orders)

