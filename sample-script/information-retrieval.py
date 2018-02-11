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

def print_market():
    r = requests.get(API_URL + "/v1/getmarkets")
    print(r.json())

def print_board():
    r = requests.get(API_URL + "/v1/getboard")
    print(r.json())

def print_ticker():
    r = requests.get(API_URL + "/v1/getticker")
    print(r.json())
    
def print_execution():
    r = requests.get(API_URL + "/v1/getexecutions")
    print(r.json())

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
    response = private_api("GET", "/v1/me/getbalance")
    print(response.json())

print_market()
print_board()
print_ticker()
print_execution()
print_balance()