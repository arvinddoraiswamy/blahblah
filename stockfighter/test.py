import requests
import os
import sys

proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/challenges/stockfighter/modules/')
sys.path.insert(0, cmd_folder)

#Importing API module
import api

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    r1= api.orderbook().json()[u'asks']
    print r1
    r1= api.orderbook().json()[u'bids']
    print r1
