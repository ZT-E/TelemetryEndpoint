import requests
from datetime import datetime
import sys
import os
import json
from addict import Dict
import time

version = "1.0.1"
print("ZT-E Serverside Module v"+version)
for x in range(5):
    x =x+1
    dot = x*'.'
    target = "Starting Up"+dot
    print(target, end='\r')
    time.sleep(2)
print(target)
print("Ready.")
print(datetime.now().strftime('%a %m-%d-%Y %H:%M:%S'))

service = ["nginx", "smbd", "ssh", "sslh", "look-glass", "zaintech"]

while True:
    r = requests.post("https://telemetry.zt-e.tech/v1/node/heartbeat")
        