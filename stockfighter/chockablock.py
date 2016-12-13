import os
import sys
import requests
import json
import random
import time
import math

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/challenges/stockfighter/modules/')
sys.path.insert(0, cmd_folder)

#Importing API module
import api

totalneeded= 760
target_price= 61.63

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    existing_orders= []
    factor= 0
    count= totalneeded

    while count >= 0:
        factor= random.randint(-2,2)
        price= int(str((math.ceil(target_price)+factor)*100)[:-2])
        num= random.randint(1,4000)
        if num <= count:
            r1= api.place_order(num, "buy", "immediate-or-cancel", price)
        else:
            num -= count
            r1= api.place_order(num, "buy", "immediate-or-cancel", price)
        l1= r1.json()
        if l1:
            existing_orders.append(l1[u'id'])

            #Check after each order before you buy again. Wait for the system to process your bid before checking.
            t1= random.randint(1,4)
            time.sleep(t1)
            for oldorder in existing_orders:
                s1= api.existing_order_status(oldorder)
                s2= s1.json()
                #If your order wasn't filled just cancel it
                if s2["totalFilled"] == 0:
                    api.cancel_order(oldorder)
                #If it was filled, see how many were filled and adjust the number you still need to buy to meet your target
                else:
                    count -= s2["totalFilled"]
            existing_orders= []

        print "Number still needed", count
