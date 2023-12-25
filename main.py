#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading, signal, time

import ST7789V
from PIL import Image,ImageDraw,ImageFont
import PIL.ImageOps
import WS2812
from rpi_ws281x import Adafruit_NeoPixel, Color

import requests
import os

dir = os.getcwd()
numpicdir = dir + "/numpic/A/"

print("1. LCD init")
BlackLightLev = 8
lcd = ST7789V.LCD1in14(BlackLightLev)
lcd.Init()
lcd.clearAll()

print("2. Set RGB Color")
rgb = WS2812.WS2812()

CL = {'White':[255,255,255], 'Red':[255,0,0], 'Green':[0,255,0], 'Blue':[0,0,255], 'Yellow':[255,255,0], 'Cyan':[0,255,255], 'Purple':[255,0,255]}
rgbColor = [CL['White'],CL['Red'],CL['Green'],CL['Blue'],CL['Yellow'],CL['Cyan']]

# rgb.Close()
rgb.SetRGB(rgbColor)

supersecretauth = 'AIzaSyDugsExa9g7-bU51rQOViFG05skGLudDlQ'
youtubeChannelId = "UCL8_FK5K4vpMGxjiyM76B4w"
youtubeUrl = f"https://www.googleapis.com/youtube/v3/channels?id={youtubeChannelId}&part=statistics&key={supersecretauth}"
updateWait = 60


def showZeroCount():
    lcd.ShowImage(0, Image.open(numpicdir + '0.jpg'))
    lcd.ShowImage(1, Image.open(numpicdir + '0.jpg'))
    lcd.ShowImage(2, Image.open(numpicdir + '0.jpg'))
    lcd.ShowImage(3, Image.open(numpicdir + '0.jpg'))
    lcd.ShowImage(4, Image.open(numpicdir + '0.jpg'))
    lcd.ShowImage(5, Image.open(numpicdir + '0.jpg'))

def getSubscriberCount(channelId: str, authKey: str):
    response = requests.get(f"https://www.googleapis.com/youtube/v3/channels?id={channelId}&part=statistics&key={authKey}")
    data: dict = response.json()
    return (data.get('items', [])[0]
            .get('statistics', {})
            .get('subscriberCount', 0))

def parseSubCount(subCount: str):
    num = float('{:.3g}'.format(int(subCount)))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def mainFun():
    print("mainThread Start")
    showZeroCount()

    while 1:
        subscriberCount = getSubscriberCount(youtubeChannelId, supersecretauth)
        displayString = parseSubCount(subscriberCount)

        # Show the correct images
        for i in range(0,len(displayString)-1):
            lcd.ShowImage(i, Image.open(numpicdir + f'{displayString[i]}.jpg'))

        time.sleep(updateWait)

mainFun()
rgb.Close()