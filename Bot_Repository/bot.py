from operator import imod
import websocket, json, pprint
import config
import talib
import numpy as np

from binance.client import Client
from binance.enums import *

RSI_PEROID = 14             # RSI 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "BNBTHB"
TRADE_QUANTITY = 0.05

SOCKET = "wss://stream.binance.com:9443/ws/bnbbtc@kline_1m"

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET, tld='us')

def order(side, quantity,symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order")
        order = client.create_order(symbol=symbol,
                                side=side,
                                type=order_type,
                                quantity=quantity)
        print(order)
    except Exception as e:
        return False
    
    return True

def on_open(ws):
    print('open connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    print('recieve message')
    #print(message)
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_close = candle['x']
    close = candle['c']

    if is_candle_close:
        print("candle closed at: {}".format(close))
        closes.append(float(close))
        print('Closed appended')
        print(closes)

        if len(closes) > RSI_PEROID:
            np_closed = np.array(closes)
            rsi = talib.RSI(np_closed, RSI_PEROID)
            print('All rsis calculated so far')
            print(rsi)
            last_rsi = rsi[-1]
            print('the current rsi is {}'.format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print('Overbought, SELL SELL SELL!!!!!')
                    # Binance order logic
                    #order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                    #    in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do")

            if last_rsi < RSI_OVERSOLD:
                # check that if we already BUY?
                if in_position:
                    print('It is oversold, but already own it, nothing to do')
                else:
                    print('Oversold, BUY BUY BUY!!!!!')
                    # Binance order logic
                    #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    #if order_succeeded:
                    #    in_position = True


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()

