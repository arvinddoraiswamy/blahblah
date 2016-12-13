import requests

venue= "RLCEX"
stock= "LCI"
account= "YPS51061980"
api_key= '9bd861ea1885ef05ae3ca66405b72c0e38c07aa2'
base_url= "https://api.stockfighter.io/ob/api/"
headers= {'X-Starfighter-Authorization': api_key}
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}

def heartbeat():
    url= base_url+'heartbeat'
    r1= requests.get(url, headers=headers, verify=False)
    return r1

def is_venue_up():
    url= base_url+'venues/'+venue+'/heartbeat'
    r1= requests.get(url, headers=headers, verify=False)
    return r1

def list_stocks_per_venue():
    url= base_url+'venues/'+venue+'/stocks'
    r1= requests.get(url, headers=headers, verify=False)
    return r1

def orderbook():
    url= base_url+'venues/'+venue+'/stocks/'+stock
    r1= requests.get(url, headers=headers, verify=False)
    return r1

def get_stock_quote():
    url =base_url+'venues/'+venue+'/stocks/'+stock+'/quote'
    r1 =requests.get(url, headers=headers, verify=False)
    return r1

def existing_order_status(orderid):
    url= base_url+'venues/'+venue+'/stocks/'+stock+'/orders/'+str(orderid)
    r1 =requests.get(url, headers=headers, verify=False)
    return r1

def status_all_orders():
    url= base_url+'venues/'+venue+'/accounts/'+account+'/orders'
    r1 =requests.get(url, headers=headers, verify=False)
    return r1

def status_all_orders_per_stock():
    url= base_url+'venues/'+venue+'/accounts/'+account+'/stocks/'+stock+'/orders'
    r1 =requests.get(url, headers=headers, verify=False)
    return r1

def place_order(quantity, direction, order_type, price):
    data= {
           "account": account,
           "venue": venue,
           "stock": stock,
           "qty": quantity,
           "price": price,
           "direction": direction,
           "orderType": order_type
    }
    url= base_url+'venues/'+venue+'/stocks/'+stock+'/orders'
    r1 =requests.post(url, headers=headers, json=data, verify=False)
    return r1

def cancel_order(orderid):
    data= {
           "venue": venue,
           "stock": stock,
           "order": orderid
    }
    url= base_url+'venues/'+venue+'/stocks/'+stock+'/orders/'+str(orderid)
    r1 =requests.delete(url, headers=headers, json=data, verify=False)
    return r1
