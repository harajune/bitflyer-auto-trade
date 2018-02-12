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

def print_execution():
    r = requests.get(API_URL + "/v1/getexecutions", 
        params={"product_code": "FX_BTC_JPY", "count": 10000})

    # print header
    print("id,side,size,exec_date,buy_child_order_acceptance_id,sell_child_order_acceptance_id")
    j = r.json()

    for v in j:
        print("%d,%s,%d,%f,%s,%s,%s" % 
                (v["id"],v["side"],v["price"],v["size"],
                v["exec_date"],v["buy_child_order_acceptance_id"],
                v["sell_child_order_acceptance_id"]))

print_execution()
