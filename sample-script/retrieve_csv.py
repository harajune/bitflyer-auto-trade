#! encoding: utf-8

import requests
import hashlib
import hmac
import yaml
import os
import json
import time

"""
load config
"""
current_dir = os.path.dirname(os.path.realpath(__file__))
config = None

with open("%s/config.yml" % current_dir, "r") as f:
    config = yaml.load(f)

"""
Constants
"""
API_URL = "https://api.bitflyer.jp"
API_KEY = config["api_key"]
API_SECRET = config["api_secret"]

def print_board():
    r = requests.get(API_URL + "/v1/getboard", params={"product_code": "FX_BTC_JPY"})

    j = r.json()

    for row in j["bids"]:
        print("bid,%f,%f" % (row["price"], row["size"]))

    print("mid,%f,0" % j["mid_price"])

    for row in j["asks"]:
        print("ask,%f,%f" % (row["price"], row["size"]))

def print_ticker():
    r = requests.get(API_URL + "/v1/getticker", params={"product_code": "FX_BTC_JPY"})

    j = r.json()

    for k, v in j.items():
        print("%s,%s" % (k, v))

    
def print_execution():
    r = requests.get(API_URL + "/v1/getexecutions", params={"product_code": "FX_BTC_JPY"})

    # print header
    print("id,side,size,exec_date,buy_child_order_acceptance_id,sell_child_order_acceptance_id")
    j = r.json()

    for v in j:
        print("%d,%s,%d,%f,%s,%s,%s" % 
                (v["id"],v["side"],v["price"],v["size"],
                v["exec_date"],v["buy_child_order_acceptance_id"],
                v["sell_child_order_acceptance_id"]))

def sign(timestamp, method, path, body=None):
    signature = hmac.new(API_SECRET.encode(), digestmod=hashlib.sha256)
    signature.update(str(timestamp).encode())
    signature.update(method.encode())
    signature.update(path.encode())
    if body is not None:
        signature.update(body.encode())

    return signature.hexdigest()

def private_api(method, path, parameters=None):
    url = API_URL + path

    timestamp = time.time()

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-TIMESTAMP": str(timestamp),
        "Content-Type": "application/json"
    }

    response = None

    if method == "GET":
        headers["ACCESS-SIGN"] = sign(timestamp, method, path)
        response = requests.get(url, headers=headers)
    elif method == "POST":
        body = json.dumps(parameters)
        headers["ACCESS-SIGN"] = sign(timestamp, method, path, body)
        response = requests.post(url, headers=headers, data=body)
    else:
        raise ValueError("method should be GET or POST.")

    return response

def print_balance():
    r = private_api("GET", "/v1/me/getbalance")
    
    # print header
    print("currency_code,amount,available")

    j = r.json()

    for row in j:
        print("%s,%f,%f" % (row["currency_code"],
            row["amount"], row["available"]))
    

def print_collateral():
    r = private_api("GET", "/v1/me/getcollateral")

    j = r.json()

    for k, v in j.items():
        print("%s,%s" % (k, v))


print_board()
print_ticker()
print_execution()
print_balance()
print_collateral()
