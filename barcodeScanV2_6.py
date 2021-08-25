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

import pygame
pygame.font.init()
display_width = 800
display_height = 480
red = (237,28,36)
green = (0,146,69)
white = (255,255,255)
screen = pygame.display.set_mode((800,480), pygame.NOFRAME)


try:
    guifile1 = "/home/pi/barcode/img/black.png"
    guigreen = pygame.image.load(guifile1).convert()
    guifile2 = "/home/pi/barcode/img/black.png"
    guired = pygame.image.load(guifile2).convert()
except:
    guifile1 = "/home/pi/barcode/img/black.png"
    guigreen = pygame.image.load(guifile1).convert()
    guifile2 = "/home/pi/barcode/img/black.png"
    guired = pygame.image.load(guifile2).convert()

def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_display(text, x, y, colour):
    largeText = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text, largeText, colour)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()



prefixAddr = "/home/pi/barcode/prefix.json"
image_file = '/home/pi/Desktop/media.png'
notExist = True
uploadUrl = 'https://faot4udb1c.execute-api.eu-west-1.amazonaws.com/live/barcode_scan'
scannerID = "1"


logging.basicConfig(level=logging.INFO, filename="/home/pi/barcode/barCodeRec.log", filemode="a", format="%(name)s - %(levelname)s - "+str(datetime.datetime.now())+" - %(message)s")
camera = PiCamera()
print("Getting prefix")

screen.blit(guigreen, (0,0))
message_display("Getting Prefixes", (display_width/2.1), (display_height/2), white)

pygame.display.update()


try:
    header={"x-api-key":"ZXj8JmRrcV42slhlCM0VW5j39nc3f40vRvFBwMlh"}
    r=requests.get("https://faot4udb1c.execute-api.eu-west-1.amazonaws.com/live/barcode_format", headers = header)
    prefixDict = json.loads(r.text)
    prefixList = prefixDict["formats"]
    with open(prefixAddr, 'w') as writeFile:
        json.dump(prefixDict, writeFile)
    print("Updated prefix list received")


    screen.blit(guigreen, (0,0))
    message_display("update prefix list recieved", (display_width/2.1), (display_height/2), white)
    pygame.display.update()


#     print(r.text)
#     for x in prefixList:
#         print(x)
except:
    with open(prefixAddr, 'r') as readFile:
        print("Prefix list read from file")
        screen.blit(guigreen, (0,0))
        message_display("prefix list read from file", (display_width/2.1), (display_height/2), white)
        pygame.display.update()

        prefixDict = json.load(readFile)
        readFile.close()
    prefixList = prefixDict["formats"]
while True:
    notExist = True
    print("Waiting for barcode")

    screen.blit(guigreen, (0,0))
    message_display("Waiting For Barcode", (display_width/2.1), (display_height/2), white)
    pygame.display.update()


    num1 = sys.stdin.readline().strip() ### This parameter will limit the multiple inctence read to one
#    num1 = "H0RS107"
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
            #time.sleep(1)
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

                screen.blit(guigreen, (0,0))
                message_display("Barcode updated in database ", (display_width/2), (display_height/2), white)
                pygame.display.flip
                pygame.display.update()

            except:
                logging.info("%s Not updated", num1)
                print("Not updated, some network issue")

                screen.blit(guigreen, (0,0))
                message_display("Not updated, some network issue", (display_width/2.1), (display_height/2), white)
                pygame.display.update()
        #time.sleep(5)
    if(notExist):
        logging.info("%s barcode is not in prefix list", num1)
        print("Barcode is not in prefix list")

        screen.blit(guigreen, (0,0))
        message_display("Barcode is not in prefix list", (display_width/2.1), (display_height/2), white)
        pygame.display.flip
        pygame.display.update()
        notExist = False
