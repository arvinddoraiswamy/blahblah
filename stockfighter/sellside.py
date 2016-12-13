import os
import sys
import time
import requests
import json
import random
from datetime import timedelta

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/challenges/stockfighter/modules/')
sys.path.insert(0, cmd_folder)

#Importing API module
import api

def get_order_qty(oid):
    s1= api.existing_order_status(oid)
    fills= s1.json()[u'fills']
    f1= [int(f1[u'qty']) for f1 in fills]
    return sum(f1)

def get_time_diff(currenttime, oldtime):
    t1= currenttime - oldtime
    diff= str(timedelta(seconds=int(t1))).split(':')[2]
    return diff

def get_current_best_price():
    r1= {}
    askprice= 0
    bidprice= 0
    askqty= 0
    bidqty= 0
    r1= api.orderbook().json()
    #Raising prices for some reason causes trouble
    if r1.has_key(u'asks') and r1[u'asks'] is not None:
        askprice= r1[u'asks'][0][u'price']
        askqty= random.randrange(40,50)
    if r1.has_key(u'bids') and r1[u'bids'] is not None:
        bidprice= r1[u'bids'][0][u'price']
        bidqty= random.randrange(40,60)

    return askprice, askqty, bidprice, bidqty

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    buy_order_track= {}
    sell_order_track= {}
    allorders= {}
    while 1:
        pos= 0
        askprice, askqty, bidprice, bidqty= get_current_best_price()

        '''
        Bid slightly higher than the best bid. Sell slightly lower than the best bid.
        '''
        #Buy shares if I haven't already hoarded a lot of shares hoping to sell them some time
        if pos <= 500:
            if bidqty != 0 and bidprice != 0:
                bidprice += 5
                print 'Buying',bidqty,'shares at ',bidprice,'$'
                r1= api.place_order(bidqty, "buy", "limit", bidprice)
                t1= time.time()
                if r1.json().has_key(u'id'):
                    buy_order_track[r1.json()[u'id']]= t1
                    allorders[r1.json()[u'id']]= "buy"
            else:
                print 'No shares available to buy. Waiting.'
        else:
            print 'Buy exception triggered',pos
            print 'Need to sell some more before you buy'

        #Sell shares if I haven't already sold a lot without actually having them
        if pos >= -500: 
            if askqty != 0 and askprice != 0:
                askprice -= 3
                print 'Selling',askqty,'shares at ',askprice,'$'
                r1= api.place_order(askqty, "sell", "limit", askprice)
                t1=time.time()
                if r1.json().has_key(u'id'):
                    sell_order_track[r1.json()[u'id']]= t1
                    allorders[r1.json()[u'id']]= "sell"
            else:
                print 'No shares available to sell. Waiting.'
        else:
            print 'Sell exception triggered',pos
            print 'Need to buy some more before you sell'

        #Get current position after buying and selling
        for oid,otype in allorders.items():
            if otype == "buy":
                pos += get_order_qty(oid)
            else:
                pos -= get_order_qty(oid)
        print 'Current pos is', pos

        #Cancel old bought shares
        for oid,oldtime in buy_order_track.items():
            currenttime= time.time()
            diff= get_time_diff(currenttime, oldtime)
            if int(diff) > 10:
                print 'Canceling order', oid
                del buy_order_track[oid]
                api.cancel_order(oid)
            else:
                continue

        #Cancel old sold shares
        for oid,oldtime in sell_order_track.items():
            currenttime= time.time()
            diff= get_time_diff(currenttime, oldtime)
            if int(diff) > 10:
                print 'Canceling order', oid
                del sell_order_track[oid]
                api.cancel_order(oid)
            else:
                continue

        print '-'* 20
