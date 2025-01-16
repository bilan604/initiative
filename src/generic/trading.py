import re
import json
import requests
from datetime import datetime

def format_price_time(price, time):
    # time is 5 hours ahead, UTC time
    price = re.sub(",", "", price)
    time = datetime.fromisoformat(time).isoformat()
    return price, time

def get_btc_price(currency):
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    resp = requests.get(url)
    obj = json.loads(resp.text)

    btc_price = obj['bpi'][currency]['rate']
    time = obj['time']['updatedISO']
    price, time = format_price_time(btc_price, time)
    return {"price": price, "time": time}

def get_btc_usd_price():    
    return get_btc_price('USD')