#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading, signal, time

import ST7789V
from PIL import Image,ImageDraw,ImageFont
import PIL.ImageOps
import BME280, math  #Atmospheric Pressure/Temperature and humidity
import WS2812 
from rpi_ws281x import Adafruit_NeoPixel, Color

import GPIOCFG
import DS3231, datetime
import os

user = "pi"

dir = os.getcwd()
if dir.count('home') == 0:
    dir = dir + "home/"+user+"/LCD-Clock-A-Code/rpi"
elif dir.count('rpi') == 0:
    dir = dir + "/LCD-Clock-A-Code/rpi"
else:
    dir = dir

numpicdir = dir + "/numpic/B/"
menupicdir = dir + "/menupic/B/"

print("1. LCD init")
BlackLightLev =  8
lcd = ST7789V.LCD1in14(BlackLightLev)
lcd.Init()
lcd.clearAll()

print("2. Set RGB Color")
rgb = WS2812.WS2812()

CL = {'White':[255,255,255], 'Red':[255,0,0], 'Green':[0,255,0], 'Blue':[0,0,255], 'Yellow':[255,255,0], 'Cyan':[0,255,255], 'Purple':[255,0,255]}
rgbColor = [CL['White'],CL['Red'],CL['Green'],CL['Blue'],CL['Yellow'],CL['Cyan']]

# rgb.Close()
rgb.SetRGB(rgbColor)

print("3. Get pressure temp hum")
bme280 = BME280.BME280()

print("4. RTC init")
rtc = DS3231.DS3231()
#   rtc.SET_Hour_Mode(24)
#rtc.SET_Time(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second) #Need to modify time zone
# rtc.SET_Time(23, 59, 55) #Need to modify time zone
# rtc.SET_Time(7, 59, 55) #Need to modify time zone

AlarmClock = [10,0,0]

gpios = GPIOCFG.GPIOCFG()

def ShowFirstTime():
    Time = rtc.Read_Time()
    
    lcd.ShowImage(0, Image.open(numpicdir + str(Time[0]//10)+'.jpg'))
    lcd.ShowImage(1, Image.open(numpicdir + str(Time[0]%10)+'.jpg'))
    lcd.ShowImage(2, Image.open(numpicdir + str(Time[1]//10)+'.jpg'))
    lcd.ShowImage(3, Image.open(numpicdir + str(Time[1]%10)+'.jpg'))
    lcd.ShowImage(4, Image.open(numpicdir + str(Time[2]//10)+'.jpg'))
    lcd.ShowImage(5, Image.open(numpicdir + str(Time[2]%10)+'.jpg'))
    
def mainFun():
    print ("mainThread Start")
    ShowFirstTime()
    
    while(1):        
        if(KeyListen() == 1):
            ShowFirstTime()
        
        Time = rtc.Read_Time()

        picsecl = numpicdir + str(Time[2]%10)+'.jpg'        
        lcd.ShowImage(5, Image.open(picsecl))
        if((Time[2]%10) == 0):  # Hh:Mm:Ss s=0, S+1
            picsech = numpicdir + str(Time[2]//10)+'.jpg'
            lcd.ShowImage(4, Image.open(picsech))
            if((Time[2]//10) == 0): # Hh:Mm:Ss S=0 m+1
                picminl = numpicdir + str(Time[1]%10)+'.jpg'
                lcd.ShowImage(3, Image.open(picminl))
                if((Time[1]%10) == 0): # Hh:Mm:Ss m=0 M+1
                    picminh = numpicdir + str(Time[1]//10)+'.jpg'
                    lcd.ShowImage(2, Image.open(picminh))
                    if((Time[1]//10) == 0): # Hh:Mm:Ss M=0 h+1
                        pichourl = numpicdir + str(Time[0]%10)+'.jpg'
                        lcd.ShowImage(1, Image.open(pichourl))                            
                        if((Time[0]%10) == 0):
                            pichourh = numpicdir + str(Time[0]//10)+'.jpg'
                            lcd.ShowImage(0, Image.open(pichourh))
                            #Update time once a day
                            rtc.SET_Time(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second) 
        
        if(AlarmClock[0] == Time[0] and AlarmClock[1] == Time[1] and AlarmClock[2] == Time[2]):
            print("Alarm Clock, beep play song....")
            gpios.BeepplaySong(3)
            Time = rtc.Read_Time()
            lcd.ShowImage(0, Image.open(numpicdir + str(Time[0]//10)+'.jpg'))
            lcd.ShowImage(1, Image.open(numpicdir + str(Time[0]%10)+'.jpg'))
            lcd.ShowImage(2, Image.open(numpicdir + str(Time[1]//10)+'.jpg'))
            lcd.ShowImage(3, Image.open(numpicdir + str(Time[1]%10)+'.jpg'))
            lcd.ShowImage(4, Image.open(numpicdir + str(Time[2]//10)+'.jpg'))
            lcd.ShowImage(5, Image.open(numpicdir + str(Time[2]%10)+'.jpg'))
    print ("beepThread Stop")
        
        
debouncetime = 0.09 #50ms debounce time, Prevent button accidental touch
MenuChoseRect = [(0,0),(133,0),(133,239),(0,239),(0,0)]  

mode_flg = 0
left_flg = 0
right_flg = 0
NowId = 1
ShowMenuFlg = 1

    
def ShowMenuFun():
    global ShowMenuFlg
    global mode_flg
    global left_flg
    global right_flg
    # global NowId
    global NowId
    LastPicId = 1
    pic1 = Image.open(menupicdir + '1.jpg')
    pic2 = Image.open(menupicdir + '2.jpg')
    pic3 = Image.open(menupicdir + '3.jpg')
    pic4 = Image.open(menupicdir + '4.jpg')
    pic5 = Image.open(menupicdir + '5.jpg')
    pic6 = Image.open(menupicdir + '6.jpg')  
    # print("Now id = %d" %NowId)
    # print("ShowMenuFlg = %d" %ShowMenuFlg)
    if(ShowMenuFlg == 1):
        ShowMenuFlg = 0
        if(NowId == 1):
            draw = ImageDraw.Draw(pic1)
        elif(NowId == 2):
            draw = ImageDraw.Draw(pic2)
        elif(NowId == 3):
            draw = ImageDraw.Draw(pic3)
        elif(NowId == 4):
            draw = ImageDraw.Draw(pic4)
        elif(NowId == 5):
            draw = ImageDraw.Draw(pic5)
        elif(NowId == 6):
            draw = ImageDraw.Draw(pic6)
        print("Show Menu")
        draw.line(MenuChoseRect, fill=255, width=10)
        lcd.ShowImage(0, pic1)
        lcd.ShowImage(1, pic2)
        lcd.ShowImage(2, pic3)
        lcd.ShowImage(3, pic4)
        lcd.ShowImage(4, pic5)
        lcd.ShowImage(5, pic6)
        
    if gpios.ReadLeftPin():
        time.sleep(debouncetime)
        if gpios.ReadLeftPin():
            while(gpios.ReadLeftPin() != 0):
                left_flg = 1
                
            LastPicId = NowId
            NowId = NowId - 1
            if(NowId == 0):
                NowId = 6
            
            print("L: NowId = %d, LastPicId = %d" %(NowId, LastPicId))
                                    
    if gpios.ReadRightPin():
        time.sleep(debouncetime)
        if gpios.ReadRightPin():
            while(gpios.ReadRightPin() != 0):
                right_flg = 1
            LastPicId = NowId
            NowId = NowId + 1
            if(NowId == 7):
                NowId = 1
            # print("R")
            # print("NowId = %d" %NowId)
            # print("LastPicId = %d" %LastPicId)
            print("R: NowId = %d, LastPicId = %d" %(NowId, LastPicId))

    if gpios.ReadModePin():
        time.sleep(debouncetime)
        if gpios.ReadModePin():
            while(gpios.ReadModePin() != 0):
                mode_flg = 1
            modelist = ["SetTime", "SetAnAlarm", "SetRGB", "SetBrightnesslevel", "ShowT&H", "Return"]
            print("Mode:", modelist[NowId-1])
            
    #show menu pic
    if(left_flg == 1 or right_flg == 1):
        NowPicName = Image.open(menupicdir + str(NowId)+ '.jpg')                
        drawNowPic = ImageDraw.Draw(NowPicName)
        drawNowPic.line(MenuChoseRect, fill=255, width=10)
        lcd.ShowImage(NowId - 1, NowPicName)                
        if(NowId != LastPicId):#first time donot show last pic,because first time not last pic
            LastPicName = Image.open(menupicdir + str(LastPicId)+ '.jpg')
            drawLastPic = ImageDraw.Draw(LastPicName)                
            lcd.ShowImage(LastPicId - 1, LastPicName)
        right_flg = 0
        left_flg = 0

def SetTimeFun():
    global mode_flg
    global left_flg
    global right_flg
    global ShowMenuFlg
    print("set time")
    TimePicId = 1
    LastTimePicId = 1
    TimeReturn = 0
    # rtc.SET_Time(12, 34, 56)
    Time = rtc.Read_Time()
    SetTimeBuf = [Time[0]//10, Time[0]%10, Time[1]//10, Time[1]%10, Time[2]//10, Time[2]%10]
    NowTimeNumpicdir = Image.open(numpicdir + str(Time[0]//10)+'.jpg')
    NowTimeNumpicdir = PIL.ImageOps.invert(NowTimeNumpicdir)
    lcd.ShowImage(0, NowTimeNumpicdir)
    lcd.ShowImage(1, Image.open(numpicdir + str(Time[0]%10)+'.jpg'))
    lcd.ShowImage(2, Image.open(numpicdir + str(Time[1]//10)+'.jpg'))
    lcd.ShowImage(3, Image.open(numpicdir + str(Time[1]%10)+'.jpg'))
    lcd.ShowImage(4, Image.open(numpicdir + str(Time[2]//10)+'.jpg'))
    lcd.ShowImage(5, Image.open(numpicdir + str(Time[2]%10)+'.jpg'))
    print("TimePicId = %d" %TimePicId)
    while(1):
        if(TimeReturn == 2):
            print("set time:break Set time mode")
            ShowMenuFlg = 1
            # Time = rtc.Read_Time()
            NewTimeBuf = [SetTimeBuf[0]*10 + SetTimeBuf[1],SetTimeBuf[2]*10 + SetTimeBuf[3], SetTimeBuf[4]*10 + SetTimeBuf[5]]
            rtc.SET_Time(NewTimeBuf[0], NewTimeBuf[1], NewTimeBuf[2])
            break
        #chose which lcd
        if gpios.ReadLeftPin():
            time.sleep(debouncetime)
            if gpios.ReadLeftPin():
                while(gpios.ReadLeftPin() != 0):
                    left_flg = 1
                LastTimePicId = TimePicId
                TimePicId = TimePicId - 1
                if(TimePicId == 0):
                    TimePicId = 6
                
                print("L: TimePicId = %d, LastTimePicId = %d" %(TimePicId,LastTimePicId))
                
        if gpios.ReadRightPin():
            time.sleep(debouncetime)
            if gpios.ReadRightPin():
                while(gpios.ReadRightPin() != 0):
                    right_flg = 1
                LastTimePicId = TimePicId
                TimePicId = TimePicId + 1
                if(TimePicId == 7):
                    TimePicId = 1
                print("R: TimePicId = %d, LastTimePicId = %d" %(TimePicId,LastTimePicId))

        if gpios.ReadModePin():
            time.sleep(debouncetime)
            if gpios.ReadModePin():
                while(gpios.ReadModePin() != 0):
                    mode_flg = 1
            print("M: change pic %d" %TimePicId)
            TimeReturn = TimeReturn + 1
            if(TimeReturn == 2):
                print("enter to change time num:break Set time mode")
                continue

        if(left_flg==1 or right_flg==1):                            
            left_flg = 0
            right_flg = 0
            NowTimeNum = SetTimeBuf[TimePicId-1]
            print("NowTimeNum = %d " %(NowTimeNum))
            
            NowTimeNumpicdir = Image.open(numpicdir + str(NowTimeNum)+'.jpg')
            NowTimeNumpicdir = PIL.ImageOps.invert(NowTimeNumpicdir)
            lcd.ShowImage(TimePicId - 1, NowTimeNumpicdir)
            if(LastTimePicId != TimePicId):
                # LastTimeNum = LastTimePicId//2
                LastTimeNum = SetTimeBuf[LastTimePicId-1]
                LastTimepicdir = Image.open(numpicdir + str(LastTimeNum)+'.jpg')
                lcd.ShowImage(LastTimePicId - 1, LastTimepicdir)
        
        while(mode_flg == 1):#enter to change time num  
            if gpios.ReadLeftPin():
                time.sleep(debouncetime)
                if gpios.ReadLeftPin():
                    while(gpios.ReadLeftPin() != 0):
                        left_flg = 1
                        TimeReturn = 0
                    OldTime = NowTimeNum
                    NowTimeNum = NowTimeNum - 1
                    print("L: time - 1: old=%d,new=%d"%(OldTime, NowTimeNum))
            if gpios.ReadRightPin():
                time.sleep(debouncetime)
                if gpios.ReadRightPin():
                    while(gpios.ReadRightPin() != 0):
                        right_flg = 1
                        TimeReturn = 0
                    OldTime = NowTimeNum
                    NowTimeNum = NowTimeNum + 1
                    print("R: time + 1: old=%d,new=%d"%(OldTime, NowTimeNum))
                        
            if gpios.ReadModePin():
                time.sleep(debouncetime)
                if gpios.ReadModePin():
                    while(gpios.ReadModePin() != 0):
                        mode_flg = 0#return ,
                    print("m: Set pic %d is OK" %(TimePicId))
                    TimeReturn = TimeReturn + 1
                    if(TimeReturn == 2):
                        print("enter to change time num:break Set time mode")
                        continue
                   
            if(left_flg==1 or right_flg==1):
                left_flg = 0
                right_flg = 0
                
                
                if(TimePicId == 1):
                    if(NowTimeNum>2):
                        NowTimeNum = 0
                    if(NowTimeNum < 0):
                        NowTimeNum = 2
                elif(TimePicId == 2):
                    if(SetTimeBuf[0]==2 and NowTimeNum>3):
                        NowTimeNum = 0
                    elif(SetTimeBuf[0]==2 and NowTimeNum<0):
                        NowTimeNum = 3
                    elif(NowTimeNum>9):
                        NowTimeNum = 0
                    elif(NowTimeNum < 0):
                        NowTimeNum = 9
                elif(TimePicId==3 or TimePicId==5):
                    if(NowTimeNum > 5):
                        NowTimeNum = 0
                    elif(NowTimeNum < 0):
                        NowTimeNum = 5
                elif(TimePicId==4 or TimePicId==6):
                    if(NowTimeNum > 9):
                        NowTimeNum = 0
                    elif(NowTimeNum < 0):
                        NowTimeNum = 9
                SetTimeBuf[TimePicId-1] = NowTimeNum
                NowTimeNumpicdir = Image.open(numpicdir + str(NowTimeNum)+'.jpg')
                NowTimeNumpicdir = PIL.ImageOps.invert(NowTimeNumpicdir)
                lcd.ShowImage(TimePicId - 1, NowTimeNumpicdir)

def SetAnAlarmFun():
    print("set An Alarm")
    global mode_flg
    global left_flg
    global right_flg
    global ShowMenuFlg
    global AlarmClock
    TimePicId = 1
    LastTimePicId = 1
    AlarmClockReturn = 0
    # AlarmClock = [8,0,0]
    # SetAlarmClockBuf = [0, 0, 0, 0, 0, 0]
    SetAlarmClockBuf = [AlarmClock[0]//10, AlarmClock[0]%10, AlarmClock[1]//10, AlarmClock[1]%10, AlarmClock[2]//10, AlarmClock[2]%10]
    NowTimeNumpicdir = Image.open(numpicdir + str(SetAlarmClockBuf[0]) + '.jpg')
    NowTimeNumpicdir = PIL.ImageOps.invert(NowTimeNumpicdir)
    lcd.ShowImage(0, NowTimeNumpicdir)
    lcd.ShowImage(1, Image.open(numpicdir + str(SetAlarmClockBuf[1]) + '.jpg'))
    lcd.ShowImage(2, Image.open(numpicdir + str(SetAlarmClockBuf[2]) + '.jpg'))
    lcd.ShowImage(3, Image.open(numpicdir + str(SetAlarmClockBuf[3]) + '.jpg'))
    lcd.ShowImage(4, Image.open(numpicdir + str(SetAlarmClockBuf[4]) + '.jpg'))
    lcd.ShowImage(5, Image.open(numpicdir + str(SetAlarmClockBuf[5]) + '.jpg'))
    print("TimePicId = %d" %TimePicId)
    while(1):
        if(AlarmClockReturn == 2):
            print("set time:break Set time mode")
            ShowMenuFlg = 1
            AlarmClock = [SetAlarmClockBuf[0]*10 + SetAlarmClockBuf[1],SetAlarmClockBuf[2]*10 + SetAlarmClockBuf[3], SetAlarmClockBuf[4]*10 + SetAlarmClockBuf[5]]
            break
        #chose which lcd
        if gpios.ReadLeftPin():
            time.sleep(debouncetime)
            if gpios.ReadLeftPin():
                while(gpios.ReadLeftPin() != 0):
                    left_flg = 1
                LastTimePicId = TimePicId
                TimePicId = TimePicId - 1
                if(TimePicId == 0):
                    TimePicId = 6
                
                print("L: TimePicId = %d, LastTimePicId = %d" %(TimePicId,LastTimePicId))
                
        if gpios.ReadRightPin():
            time.sleep(debouncetime)
            if gpios.ReadRightPin():
                while(gpios.ReadRightPin() != 0):
                    right_flg = 1
                LastTimePicId = TimePicId
                TimePicId = TimePicId + 1
                if(TimePicId == 7):
                    TimePicId = 1
                print("R: TimePicId = %d, LastTimePicId = %d" %(TimePicId,LastTimePicId))

        if gpios.ReadModePin():
            time.sleep(debouncetime)
            if gpios.ReadModePin():
                while(gpios.ReadModePin() != 0):
                    mode_flg = 1
            print("M: change pic %d" %TimePicId)
            AlarmClockReturn = AlarmClockReturn + 1
            if(AlarmClockReturn == 2):
                print("enter to change time num:break Set time mode")
                continue

        if(left_flg==1 or right_flg==1):                            
            left_flg = 0
            right_flg = 0
            NowAlarmClockNum = SetAlarmClockBuf[TimePicId-1]
            print("NowAlarmClockNum = %d " %(NowAlarmClockNum))
            
            NowAlarmClockNumpicdir = Image.open(numpicdir + str(NowAlarmClockNum)+'.jpg')
            NowAlarmClockNumpicdir = PIL.ImageOps.invert(NowAlarmClockNumpicdir)
            lcd.ShowImage(TimePicId - 1, NowAlarmClockNumpicdir)
            if(LastTimePicId != TimePicId):
                # LastTimeNum = LastTimePicId//2
                LastTimeNum = SetAlarmClockBuf[LastTimePicId-1]
                LastTimepicdir = Image.open(numpicdir + str(LastTimeNum)+'.jpg')
                lcd.ShowImage(LastTimePicId - 1, LastTimepicdir)
        
        while(mode_flg == 1):#enter to change time num  
            if gpios.ReadLeftPin():
                time.sleep(debouncetime)
                if gpios.ReadLeftPin():
                    while(gpios.ReadLeftPin() != 0):
                        left_flg = 1
                        AlarmClockReturn = 0
                    OldTime = NowAlarmClockNum
                    NowAlarmClockNum = NowAlarmClockNum - 1
                    print("L: time - 1: old=%d,new=%d"%(OldTime, NowAlarmClockNum))
            if gpios.ReadRightPin():
                time.sleep(debouncetime)
                if gpios.ReadRightPin():
                    while(gpios.ReadRightPin() != 0):
                        right_flg = 1
                        AlarmClockReturn = 0
                    OldTime = NowAlarmClockNum
                    NowAlarmClockNum = NowAlarmClockNum + 1
                    print("R: time + 1: old=%d,new=%d"%(OldTime, NowAlarmClockNum))
                        
            if gpios.ReadModePin():
                time.sleep(debouncetime)
                if gpios.ReadModePin():
                    while(gpios.ReadModePin() != 0):
                        mode_flg = 0#return ,
                    print("m: Set pic %d is OK" %(TimePicId))
                    AlarmClockReturn = AlarmClockReturn + 1
                    if(AlarmClockReturn == 2):
                        print("enter to change time num:break Set time mode")
                        continue
                   
            if(left_flg==1 or right_flg==1):
                left_flg = 0
                right_flg = 0
                if(TimePicId == 1):
                    if(NowAlarmClockNum>2):
                        NowAlarmClockNum = 0
                    if(NowAlarmClockNum < 0):
                        NowAlarmClockNum = 2
                elif(TimePicId == 2):
                    if(SetAlarmClockBuf[0]==2 and NowAlarmClockNum>3):
                        NowAlarmClockNum = 0
                    elif(SetAlarmClockBuf[0]==2 and NowAlarmClockNum<0):
                        NowAlarmClockNum = 3
                    elif(NowAlarmClockNum>9):
                        NowAlarmClockNum = 0
                    elif(NowAlarmClockNum < 0):
                        NowAlarmClockNum = 9
                elif(TimePicId==3 or TimePicId==5):
                    if(NowAlarmClockNum > 5):
                        NowAlarmClockNum = 0
                    elif(NowAlarmClockNum < 0):
                        NowAlarmClockNum = 5
                elif(TimePicId==4 or TimePicId==6):
                    if(NowAlarmClockNum > 9):
                        NowAlarmClockNum = 0
                    elif(NowAlarmClockNum < 0):
                        NowAlarmClockNum = 9
                SetAlarmClockBuf[TimePicId-1] = NowAlarmClockNum
                NowAlarmClockNumpicdir = Image.open(numpicdir + str(NowAlarmClockNum)+'.jpg')
                NowAlarmClockNumpicdir = PIL.ImageOps.invert(NowAlarmClockNumpicdir)
                lcd.ShowImage(TimePicId - 1, NowAlarmClockNumpicdir)

def SetRGBFun():
    print("Set RGB")
    global mode_flg
    global left_flg
    global right_flg
    global ShowMenuFlg
    
    RGBPicId = 1
    LastSetrgbPicId = 1
    SetRGBReturn = 0
    CLNum = 1 #first rgb color list 
    # rtc.SET_Time(12, 34, 56)
    Time = rtc.Read_Time()
    imageSetRgb1 = Image.new("RGB", (135,240), "WHITE")
    drawSetRgb = ImageDraw.Draw(imageSetRgb1)
    drawSetRgb.line([(30,80),(100,80),(100,150),(30,150),(30,80)], fill=(100,100,100), width=10)
    drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[0][0], rgbColor[0][1], rgbColor[0][2]))
    drawSetRgb.line(MenuChoseRect, fill=255, width=10)
    lcd.clearAll()
    lcd.ShowImage(0, imageSetRgb1)
    drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[1][0], rgbColor[1][1], rgbColor[1][2]))
    drawSetRgb.line(MenuChoseRect, fill=0, width=10)
    lcd.ShowImage(1, imageSetRgb1)
    drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[2][0], rgbColor[2][1], rgbColor[2][2]))
    lcd.ShowImage(2, imageSetRgb1)
    drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[3][0], rgbColor[3][1], rgbColor[3][2]))
    lcd.ShowImage(3, imageSetRgb1)
    drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[4][0], rgbColor[4][1], rgbColor[4][2]))
    lcd.ShowImage(4, imageSetRgb1)
    drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[5][0], rgbColor[5][1], rgbColor[5][2]))
    lcd.ShowImage(5, imageSetRgb1)
    print("RGBPicId = %d" %RGBPicId)
    while(1):
        if(SetRGBReturn == 2):
            print("break1: RGB mode")
            ShowMenuFlg = 1
            break
        #chose which lcd
        if gpios.ReadLeftPin():
            time.sleep(debouncetime)
            if gpios.ReadLeftPin():
                while(gpios.ReadLeftPin() != 0):
                    left_flg = 1
                    SetRGBReturn = 0                   
                LastSetrgbPicId = RGBPicId
                RGBPicId = RGBPicId - 1
                if(RGBPicId == 0):
                    RGBPicId = 6
                print("L: RGBPicId = %d, LastSetrgbPicId = %d" %(RGBPicId,LastSetrgbPicId))
                
        if gpios.ReadRightPin():
            time.sleep(debouncetime)
            if gpios.ReadRightPin():
                while(gpios.ReadRightPin() != 0):
                    right_flg = 1
                    SetRGBReturn = 0
                LastSetrgbPicId = RGBPicId
                RGBPicId = RGBPicId + 1
                if(RGBPicId == 7):
                    RGBPicId = 1
                print("R: RGBPicId = %d, LastSetrgbPicId = %d" %(RGBPicId,LastSetrgbPicId))

        if gpios.ReadModePin():
            time.sleep(debouncetime)
            if gpios.ReadModePin():
                while(gpios.ReadModePin() != 0):
                    mode_flg = 1
                print("M: change RGB NUM:%d" %RGBPicId)
                SetRGBReturn = SetRGBReturn + 2

        if(left_flg==1 or right_flg==1):                            
            left_flg = 0
            right_flg = 0
            
            drawSetRgb.line(MenuChoseRect, fill=255, width=10)
            drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[RGBPicId-1][0],rgbColor[RGBPicId-1][1],rgbColor[RGBPicId-1][2]))
            # drawSetRgb.rectangle([30,80,100,150],fill = (255,0,0))
            lcd.ShowImage(RGBPicId - 1, imageSetRgb1)
            if(LastSetrgbPicId != RGBPicId):
                # LastTimeNum = LastSetrgbPicId//2
                drawSetRgb.line(MenuChoseRect, fill=0, width=10)
                drawSetRgb.rectangle([30,80,100,150],fill = (rgbColor[LastSetrgbPicId-1][0],rgbColor[LastSetrgbPicId-1][1],rgbColor[LastSetrgbPicId-1][2]))
                lcd.ShowImage(LastSetrgbPicId - 1, imageSetRgb1)
        
        while(mode_flg == 1):#enter to change time num  
            if gpios.ReadLeftPin():
                time.sleep(debouncetime)
                if gpios.ReadLeftPin():
                    while(gpios.ReadLeftPin() != 0):
                        left_flg = 1
                        SetRGBReturn = 0
                    # OldRgbColorId = RGBPicId
                    CLNum = CLNum - 1
                    if(CLNum == 0):
                        CLNum = 7
                    print("L: color<<%d"%(CLNum))
            if gpios.ReadRightPin():
                time.sleep(debouncetime)
                if gpios.ReadRightPin():
                    while(gpios.ReadRightPin() != 0):
                        right_flg = 1
                        SetRGBReturn = 0
                    CLNum = CLNum + 1
                    if(CLNum == 8):
                        CLNum = 1
                    # CLNum = CLNum + 1
                    print("R: color>>%d"%(CLNum))
            if gpios.ReadModePin():
                time.sleep(debouncetime)
                if gpios.ReadModePin():
                    while(gpios.ReadModePin() != 0):
                        mode_flg = 0#return ,
                    print("M: Set RGB Pixel %d is OK" %(RGBPicId))
                    # SetRGBReturn = 0
                    # if(SetRGBReturn == 3):
                        # print("break2: SET RGB COLOR")
                        # continue
                   
            if(left_flg==1 or right_flg==1):
                left_flg = 0
                right_flg = 0
                # SetRGBReturn = 0
                drawSetRgb.rectangle([30,80,100,150],fill = (list(CL.values())[CLNum-1][0],list(CL.values())[CLNum-1][1],list(CL.values())[CLNum-1][2]))
                # drawSetRgb.rectangle([30,80,100,150],fill = (255,0,0))
                drawSetRgb.line(MenuChoseRect, fill=255, width=10)
                lcd.ShowImage(RGBPicId - 1, imageSetRgb1)
            # if(mode_flg == 1):
                # print("pixel %d old rgb color %s" %(RGBPicId, ))
                oldcolor = rgbColor[RGBPicId - 1]
                rgbColor[RGBPicId-1] = list(CL.values())[CLNum-1]
                # print("newrgb color",rgbColor)
                print("pixel %d color change %s->%s" %(RGBPicId, oldcolor, rgbColor[RGBPicId-1]))
                rgb.SetPixelColor(RGBPicId-1, rgbColor[RGBPicId-1])
        
def SetBLFun():
    print("Set LCD light")
    global mode_flg
    global left_flg
    global right_flg
    global ShowMenuFlg
    global BlackLightLev
    
    # BlackLightLev = 1
    # LastSetBlackLightLev = 1
    SetLcdBLReturn = 0
    lcd.ShowImage(0, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
    lcd.ShowImage(1, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
    lcd.ShowImage(2, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
    lcd.ShowImage(3, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
    lcd.ShowImage(4, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
    lcd.ShowImage(5, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
    print("BlackLightLev = %d" %BlackLightLev)
    while(1):
        if(SetLcdBLReturn == 2):
            print("break1: Black Light Lev")
            ShowMenuFlg = 1
            break
        #chose which lcd
        if gpios.ReadLeftPin():
            time.sleep(debouncetime)
            if gpios.ReadLeftPin():
                while(gpios.ReadLeftPin() != 0):
                    left_flg = 1
                    SetLcdBLReturn = 0                   
                # LastSetBlackLightLev = BlackLightLev
                BlackLightLev = BlackLightLev - 1
                if(BlackLightLev == 0):
                    BlackLightLev = 9
                print("L: BlackLightLev = %d" %(BlackLightLev))
                
        if gpios.ReadRightPin():
            time.sleep(debouncetime)
            if gpios.ReadRightPin():
                while(gpios.ReadRightPin() != 0):
                    right_flg = 1
                    SetLcdBLReturn = 0
                # LastSetBlackLightLev = BlackLightLev
                BlackLightLev = BlackLightLev + 1
                if(BlackLightLev == 10):
                    BlackLightLev = 1
                print("R: BlackLightLev = %d" %(BlackLightLev))

        if gpios.ReadModePin():
            time.sleep(debouncetime)
            if gpios.ReadModePin():
                while(gpios.ReadModePin() != 0):
                    mode_flg = 0
                print("M: change RGB NUM:%d" %BlackLightLev)
                SetLcdBLReturn = SetLcdBLReturn + 1

        if(left_flg==1 or right_flg==1):                            
            left_flg = 0
            right_flg = 0
            lcd.ShowImage(0, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
            lcd.ShowImage(1, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
            lcd.ShowImage(2, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
            lcd.ShowImage(3, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
            lcd.ShowImage(4, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
            lcd.ShowImage(5, Image.open(numpicdir + str(BlackLightLev)+'.jpg'))
            lcd.SetLcdBlackLight(BlackLightLev)
        
def ShowTemHumFun():
    print("Show Tem Hum ")
    bme280.get_calib_param()
    bme = []
    bme = bme280.readData()
    pressure = round(bme[0], 2) 
    temp = round(bme[1], 2) 
    hum = round(bme[2], 2)
    
    showTHPtime = 2

    # print("pressure : %7.2f hPa" %pressure)
    print("temp : %-6.2f ℃" %temp)
    print("hum : %6.2f ％" %hum)
    # Prelist = list(str(pressure))
    Templist = list(str(temp))
    Humlist = list(str(hum))
    # print("pressure", Prelist)
    # print("temp", Templist)
    # print("hum", Humlist)
    
    font1 = ImageFont.truetype(('Font.ttc'), 200)
    font2 = ImageFont.truetype(('Font.ttc'), 150)
    xoffset = 10
    yoffset = 0
    
    imageShowTH = Image.new("RGB", (135,240), "WHITE")
    drawTemHum = ImageDraw.Draw(imageShowTH)
    drawTemHum.text((xoffset, yoffset), str(Templist[0]), font = font1, fill = "red")
    lcd.ShowImage(0, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Templist[1]), font = font1, fill = "red")
    lcd.ShowImage(1, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Templist[2]), font = font1, fill = "red")
    lcd.ShowImage(2, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Templist[3]), font = font1, fill = "red")
    lcd.ShowImage(3, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Templist[4]), font = font1, fill = "red")
    lcd.ShowImage(4, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), "C", font = font1, fill = "red")
    lcd.ShowImage(5, imageShowTH)
    
    time.sleep(showTHPtime)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Humlist[0]), font = font1, fill = "blue")
    lcd.ShowImage(0, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Humlist[1]), font = font1, fill = "blue")
    lcd.ShowImage(1, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Humlist[2]), font = font1, fill = "blue")
    lcd.ShowImage(2, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Humlist[3]), font = font1, fill = "blue")
    lcd.ShowImage(3, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")
    drawTemHum.text((xoffset, yoffset), str(Humlist[4]), font = font1, fill = "blue")
    lcd.ShowImage(4, imageShowTH)
    drawTemHum.rectangle((0, 0, 135, 240), fill = "white")    
    drawTemHum.text((xoffset, yoffset+30), "%", font = font2, fill = "blue")
    lcd.ShowImage(5, imageShowTH)
    time.sleep(showTHPtime)
    
    global ShowMenuFlg
    ShowMenuFlg = 1
    return

   
def KeyListen():
    global mode_flg
    global left_flg
    global right_flg    
    global NowId
    global ShowMenuFlg
    
    if(gpios.ReadModePin() != 0):
        time.sleep(debouncetime)
        if gpios.ReadModePin():
            while(gpios.ReadModePin() != 0):
                mode_flg = 0
        # pic1 = Image.new('RGB', (135, 240), "WHITE") 
   
        print ("KeyListen Start")      
        while(1):
            ShowMenuFun()
                
            if(mode_flg == 1):#mode key is down
                mode_flg = 0
                if(NowId == 1):#set time
                    SetTimeFun()
            
                if(NowId == 2):#Set AnAlarm
                    SetAnAlarmFun()
                    
                if(NowId == 3):
                    SetRGBFun()
                    
                if(NowId == 4):
                    SetBLFun()
                
                if(NowId == 5):
                    ShowTemHumFun()
                    
                if(NowId == 6):#return
                    # ReturnFun()
                    ShowMenuFlg = 1
                    NowId = 1
                    ShowFirstTime()
                    # KeyListenFlg = 0
                    return 1
        return 0
                    

mainFun()

rgb.Close()
gpios.Beep()
gpios.destory()
