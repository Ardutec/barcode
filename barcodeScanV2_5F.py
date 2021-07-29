#!/usr/bin/python3
import binascii
import os
import requests
import sys
import time
import datetime
from picamera import PiCamera
import logging
import json
import base64
from requests_toolbelt import MultipartEncoder

prefixAddr = "/home/pi/barcode/prefix.json"
image_file = '/home/pi/Desktop/media.png'
notExist = True
uploadUrl = 'https://faot4udb1c.execute-api.eu-west-1.amazonaws.com/live/barcode_scan'
scannerID = "1"


logging.basicConfig(level=logging.INFO, filename="/home/pi/barcode/barCodeRec.log", filemode="a", format="%(name)s - %(levelname)s - "+str(datetime.datetime.now())+" - %(message)s")
camera = PiCamera()
print("Getting prefix")
try:
    header={"x-api-key":"ZXj8JmRrcV42slhlCM0VW5j39nc3f40vRvFBwMlh"}
    r=requests.get("https://faot4udb1c.execute-api.eu-west-1.amazonaws.com/live/barcode_format", headers = header)
    prefixDict = json.loads(r.text)
    prefixList = prefixDict["formats"]
    with open(prefixAddr, 'w') as writeFile:
        json.dump(prefixDict, writeFile)
    print("Updated prefix list received")
#     print(r.text)
#     for x in prefixList:
#         print(x)
except:
    with open(prefixAddr, 'r') as readFile:
        print("Prefix list read from file")
        prefixDict = json.load(readFile)
        readFile.close()
    prefixList = prefixDict["formats"]
while True:
    notExist = True
    print("Waiting for barcode")
    num1 = sys.stdin.readline().strip() ### This parameter will limit the multiple inctence read to one
#     num1 = "H0RS107"
#     print(num1)
#     print(len(num1))
    now = int(round(time.time() * 1000))
    for x in prefixList:
        pl = len(x)
        prefix = num1[0:pl]
        if(x==prefix):
            notExist = False
            camera.start_preview()
            camera.capture(image_file)
            camera.stop_preview()
            fields = {
                'barcode': num1,
                'scanner_id': scannerID,
                'timestamp': str(now),
                'image': (image_file, open(image_file, 'rb'), 'image/png')
            }
            payload = MultipartEncoder(fields, boundary='test')
            header={
                "x-api-key":"ZXj8JmRrcV42slhlCM0VW5j39nc3f40vRvFBwMlh",
                "Accept": 'multipart/form-data',
                "Content-Type": payload.content_type,
            }
            try:
                r=requests.post(uploadUrl, headers=header, data=payload,)
                logging.info("%s updated in database", num1)
                print(r.text)
                print(r.status_code)
            except:
                logging.info("%s Not updated", num1)
                print("Not updated, some network issue")
#             time.sleep(10)
    if(notExist):
        logging.info("%s barcode is not in prefix list", num1)
        print("Barcode is not in prefix list")
        notExist = False
