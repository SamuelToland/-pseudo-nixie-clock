#!/usr/bin/python
# -*- coding:utf-8 -*-
import spidev as SPI
import RPi.GPIO as GPIO
import time
import numpy as np
       
class LCD1in14():
    def __init__(self, bllev):
        self.width = 135
        self.height = 240 
        
        self.DC_PIN = 25
        self.BL_PIN =24
        self.RST_PIN = 27
        
        self.CSA1_PIN = 16 #74HC138 a1
        self.CSA2_PIN = 20
        self.CSA3_PIN = 21
        
        self.blacklight = bllev
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.DC_PIN,GPIO.OUT)
        GPIO.setup(self.RST_PIN,GPIO.OUT)
        GPIO.setup(self.BL_PIN,GPIO.OUT)
        # GPIO.output(self.BL_PIN, 1)
        self.Blight = GPIO.PWM(self.BL_PIN, 100)
        self.Blight.start(0)
        # self.Blight.ChangeDutyCycle(20)
        self.SetLcdBlackLight(self.blacklight)
        
        GPIO.setup(self.CSA1_PIN, GPIO.OUT)
        GPIO.setup(self.CSA2_PIN, GPIO.OUT)
        GPIO.setup(self.CSA3_PIN, GPIO.OUT)
        GPIO.output(self.CSA1_PIN, 1)
        GPIO.output(self.CSA2_PIN, 1)
        GPIO.output(self.CSA3_PIN, 1)
        
        #Initialize SPI
        self.spi = SPI.SpiDev(0, 0)
        self.spi.max_speed_hz = 40000000
        
    def SetLcdBlackLight(self, lev):#0-10
        self.Blight.ChangeDutyCycle(lev*10)
                
    def digital_write(self, pin, val):
        GPIO.output(pin, val)
        
    def lcd_cs_l(self, lnum):
        # if(self.mode == 1):
        lnum = 5 - lnum
        GPIO.output(self.CSA1_PIN, lnum&0x01)
        GPIO.output(self.CSA2_PIN, (lnum>>1)&0x01)
        GPIO.output(self.CSA3_PIN, (lnum>>2)&0x01)
        
    def lcd_cs_h(self, lnum):
        # if(self.mode == 1):
        lnum = 5 - lnum
        GPIO.output(self.CSA1_PIN, 1)
        GPIO.output(self.CSA2_PIN, 1)
        GPIO.output(self.CSA3_PIN, 1)

    def command(self, lnum, cmd):
        self.digital_write(self.DC_PIN, 0)
        self.lcd_cs_l(lnum)
        self.spi.writebytes([cmd])
        self.lcd_cs_h(lnum)
        
    def data(self, lnum, val):
        self.digital_write(self.DC_PIN, 1)
        self.lcd_cs_l(lnum)
        self.spi.writebytes([val])
        self.lcd_cs_h(lnum)

    def commandAll(self, cmd):
        self.digital_write(self.DC_PIN, 0)
        for num in range(0, 6):
            self.lcd_cs_l(num)
            self.spi.writebytes([cmd])
            self.lcd_cs_h(num)
        
    def dataAll(self, val):
        self.digital_write(self.DC_PIN, 1)
        for num in range(0, 6):
            self.lcd_cs_l(num)
            self.spi.writebytes([val])
            self.lcd_cs_h(num)
        
    def reset(self):
        """Reset the display"""
        GPIO.output(self.RST_PIN, 1)
        time.sleep(0.01)
        GPIO.output(self.RST_PIN, 0)
        time.sleep(0.1)
        GPIO.output(self.RST_PIN, 1)
        time.sleep(0.01)
        
    def Init(self):
        """Initialize dispaly"""  
        # self.module_init()
        self.reset()

        self.commandAll(0x36)
        self.dataAll(0x10)                 #self.dataAll(0x00)

        self.commandAll(0x3A) 
        self.dataAll(0x05)

        self.commandAll(0xB2)
        self.dataAll(0x0C)
        self.dataAll(0x0C)
        self.dataAll(0x00)
        self.dataAll(0x33)
        self.dataAll(0x33)

        self.commandAll(0xB7)
        self.dataAll(0x35) 

        self.commandAll(0xBB)
        self.dataAll(0x19)

        self.commandAll(0xC0)
        self.dataAll(0x2C)

        self.commandAll(0xC2)
        self.dataAll(0x01)

        self.commandAll(0xC3)
        self.dataAll(0x12)   

        self.commandAll(0xC4)
        self.dataAll(0x20)

        self.commandAll(0xC6)
        self.dataAll(0x0F) 

        self.commandAll(0xD0)
        self.dataAll(0xA4)
        self.dataAll(0xA1)

        self.commandAll(0xE0)
        self.dataAll(0xD0)
        self.dataAll(0x04)
        self.dataAll(0x0D)
        self.dataAll(0x11)
        self.dataAll(0x13)
        self.dataAll(0x2B)
        self.dataAll(0x3F)
        self.dataAll(0x54)
        self.dataAll(0x4C)
        self.dataAll(0x18)
        self.dataAll(0x0D)
        self.dataAll(0x0B)
        self.dataAll(0x1F)
        self.dataAll(0x23)

        self.commandAll(0xE1)
        self.dataAll(0xD0)
        self.dataAll(0x04)
        self.dataAll(0x0C)
        self.dataAll(0x11)
        self.dataAll(0x13)
        self.dataAll(0x2C)
        self.dataAll(0x3F)
        self.dataAll(0x44)
        self.dataAll(0x51)
        self.dataAll(0x2F)
        self.dataAll(0x1F)
        self.dataAll(0x1F)
        self.dataAll(0x20)
        self.dataAll(0x23)
        
        self.commandAll(0x21)

        self.commandAll(0x11)

        self.commandAll(0x29)
    
    def SetWindowsAll(self, Xstart, Ystart, Xend, Yend):
        xadd = 52
        yadd = 40
        self.commandAll(0x2A)
        self.dataAll((Xstart+xadd)>>8& 0xff)
        self.dataAll((Xstart+xadd)   & 0xff)
        self.dataAll((Xend-1+xadd)>>8& 0xff)
        self.dataAll((Xend-1+xadd)   & 0xff)
        
        self.commandAll(0x2B)
        self.dataAll((Ystart+yadd)>>8& 0xff)
        self.dataAll((Ystart+yadd)   & 0xff)
        self.dataAll((Yend-1+yadd)>>8& 0xff)
        self.dataAll((Yend-1+yadd)   & 0xff)
        
        self.commandAll(0x2C)
        # self.commandAll(0x2A)
        # self.dataAll(0x00)
        # self.dataAll(0x34)
        # self.dataAll(0x00)
        # self.dataAll(0xBa)
        
        # self.commandAll(0x2B)
        # self.dataAll(0x00)
        # self.dataAll(0x28)
        # self.dataAll(0x01)
        # self.dataAll(0x17)
        
        # self.commandAll(0x2C)
    
    def SetWindows(self, lnum, Xstart, Ystart, Xend, Yend):
        xadd = 52
        yadd = 40
        self.command(lnum, 0x2A)
        self.data(lnum, (Xstart+xadd)>>8& 0xff)               #Set the horizontal starting point to the high octet
        self.data(lnum, (Xstart+xadd)   & 0xff)      #Set the horizontal starting point to the low octet
        self.data(lnum, (Xend-1+xadd)>>8& 0xff)        #Set the horizontal end to the high octet
        self.data(lnum, (Xend-1+xadd)   & 0xff) #Set the horizontal end to the low octet 
        # self.dataAll(0x00)
        # self.dataAll(0x34)
        # self.dataAll(0x00)
        # self.dataAll(0xBa)
        self.command(lnum, 0x2B)
        self.data(lnum, (Ystart+yadd)>>8& 0xff)
        self.data(lnum, (Ystart+yadd)   & 0xff)
        self.data(lnum, (Yend-1+yadd)>>8& 0xff)
        self.data(lnum, (Yend-1+yadd)   & 0xff)
        # self.dataAll(0x00)
        # self.dataAll(0x28)
        # self.dataAll(0x01)
        # self.dataAll(0x17)
        self.command(lnum,0x2C) 

        
    def ShowImage(self, lnum, Image):
        imwidth, imheight = Image.size
        # print(imwidth)
        # print(imheight)
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = np.asarray(Image) #data is 
        # [[[R G B C]...*135W...[R G B C] []]
        #.
        #.*240 
        #.[[[R G B C]...*135W...[R G B C] []]
        pix = np.zeros((240, 135, 2), dtype = np.uint8)#zeros(h,w,bytes)
        # RGB88->RGB565  r=8->R&&11111000 
        pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8), np.right_shift(img[...,[1]], 5))
        pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0), np.right_shift(img[...,[2]],3))
        
        pix = pix.flatten().tolist()
        self.SetWindows(lnum,  0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN, 1)
        # print(len(pix))
        self.lcd_cs_l(lnum)
        for i in range(0,len(pix),4096):
            self.spi.writebytes(pix[i:i+4096])
        self.lcd_cs_h(lnum)

    def clear(self, lnum):
        """Clear contents of image buffer"""
        _buffer = [0xFF]*(self.width * self.height * 2)
        self.SetWindows(lnum, 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN, 1)
        self.lcd_cs_l(num)
        for i in range(0,len(_buffer),4096):
            # self.lcd_cs_l(lnum)
            self.spi.writebytes(_buffer[i:i+4096])
        self.lcd_cs_h(num)
    
    def clearAll(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindowsAll(0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN, 1)
        for num in range(0, 6):
            self.lcd_cs_l(num)
            for i in range(0,len(_buffer),4096):                
                self.spi.writebytes(_buffer[i:i+4096])
            self.lcd_cs_h(num)
            
            
if __name__=='__main__':
    print("LCD test")

    LCD = LCD1in14(1)
    LCD.clearAll()