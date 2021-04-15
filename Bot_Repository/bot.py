from operator import imod
import websocket, json, pprint
import config
import talib
import numpy as np

from binance.client import Client
from binance.enums import *

RSI_PEROID = 14             # RSI 14
RSI_OVERBOUGHT = 70         # Overbought threshold
RSI_OVERSOLD = 30           # Oversold threshold
TRADE_SYMBOL = "BNBBUSD"    # Coin pair
TRADE_QUANTITY = 0.03       # Coin quantity **Buy quantity will be the same as sell quantity 
                            # ex. 0.03 meaning that we will buy BNB 0.03 coin and will sell BNB 0.03 coin also.
   
SOCKET = "wss://stream.binance.com:9443/ws/bnbbusd@kline_1m"

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity,symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order")
        #order = client.create_order(symbol=symbols, side=sides, type=order_type, quantity=quantitys)
        #orders = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        #print(orders)
        print('Order complete')
    except Exception as e:
        print('Something wrong')
        return False
    
    return True

def on_open(ws):
    print('open connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position

    print('recieve message')
    #print(message)
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_close = candle['x']
    close = candle['c']
    
    #####   Condition RSI depend on RSI_PEROID ######
    ##### START ######
    if is_candle_close:
        print("candle closed at: {}".format(close))
        closes.append(float(close))
        print('Closed appended')
        #print(closes)

        if len(closes) > RSI_PEROID:
            np_closed = np.array(closes)
            rsi = talib.RSI(np_closed, RSI_PEROID)
            print('All rsis calculated so far')
            print(rsi)
            last_rsi = rsi[-1]
            print('the current rsi is {}'.format(last_rsi))
    ##### END ######

    #####   BUY - SELL condition  #####################
    ##### START ######           
            if (last_rsi > RSI_OVERBOUGHT):
                print("Overbought Loop")
                if in_position:
                    print('Overbought, SELL SELL SELL!!!!!')
                    # Binance order logic
                    Succeed = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if Succeed:
                        in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do")
                #print('we are in the loop bought')
                
            if (last_rsi < RSI_OVERSOLD):
                # check that if we already BUY?
                print('Oversold Loop')
                if in_position:
                    print('It is oversold, but already own it, nothing to do')
                else:
                    print('Oversold, BUY BUY BUY!!!!!')
                    # Binance order logic
                    Succeed = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if Succeed:
                        in_position = True
                #print('we are in the loop Sold')
    ##### END ######

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()

