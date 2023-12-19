#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time

# 定义低中高频率
CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes
CM = [0, 262, 294, 330, 349, 392, 440, 494]		# Frequency of Middle C notes
CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes
CHH = [0, 1046, 1175, 1318, 1397, 1568, 1760, 1976]

metre = 0.2

song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]
beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			# Beats of song 1, 1 means 1/8 beats
			1, 1, 1, 1, 1, 1, 3, 1, 
			1, 3, 1, 1, 1, 1, 1, 1, 
			1, 2, 1, 1, 1, 1, 1, 1, 
			1, 1, 3	]
song_2 = [	CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
			CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
			CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
			CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]
 
beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			# Beats of song 2, 1 means 1/8 beats
			1, 1, 2, 2, 1, 1, 3, 1, 
			1, 2, 2, 1, 1, 2, 2, 1, 
			1, 2, 2, 1, 1, 3 ]

            # Tone 0 is a rest
song_3 = [
    CM[1],CM[2],CM[3],CM[5],CM[5],CM[0],CM[3],CM[2],CM[1],CM[2],CM[3],CM[0],
    CM[1],CM[2],CM[3],CM[7],CH[1],CH[1],CH[1],CM[7],CH[1],CM[7],CM[6],CM[5],CM[0],
    CM[1],CM[2],CM[3],CM[5],CM[5],CM[0],CM[3],CM[2],CM[1],CM[2],CM[1],CM[0],
    CM[1],CM[2],CM[3],CM[5],CM[1],CM[0],CM[1],CL[7],CL[6],CL[7],CM[1],CM[0]
]
# beat corresponding to pitch
beat_3 = [
    2,2,2,1,5,4,2,2,2,1,5,4,
    2,2,2,1,5,2,2,2,1,3,2,4,4,
    2,2,2,1,5,4,2,2,2,1,3,5,
    2,2,2,1,5,4,2,2,2,2,8,2
]

class GPIOCFG:
    def __init__(self):        
        self.MODE_PIN = 26
        self.LEFT_PIN = 22
        self.RIGHT_PIN =  17     
        self.BEPP_PIN = 13
                
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.MODE_PIN,    GPIO.IN) 
        GPIO.setup(self.LEFT_PIN,    GPIO.IN) 
        GPIO.setup(self.RIGHT_PIN,   GPIO.IN) 
        GPIO.setup(self.BEPP_PIN,   GPIO.OUT) 
        
        self.Buzz = GPIO.PWM(self.BEPP_PIN, 440)
        self.Buzz.start(100)
        
    def ReadModePin(self):
        val = GPIO.input(self.MODE_PIN)
        if(val != 0):
            self.Beep(CM[1])
        return val
    def ReadLeftPin(self):
        val = GPIO.input(self.LEFT_PIN)
        if(val != 0):
            self.Beep(CM[3])
        return val
    def ReadRightPin(self):
        val = GPIO.input(self.RIGHT_PIN)
        if(val != 0):
            self.Beep(CM[5])
        return val

    def Beep(self, fre):
        self.Buzz.start(50)
        self.Buzz.ChangeFrequency(fre) # Change the frequency along the song note
        time.sleep(0.001)     # delay a note for beat * 0.5s
        # self.Buzz.start(30)
        # self.Buzz.start(10)
        self.Buzz.start(0)
        
    def BeepplaySong(self, whichmusic):
        if(whichmusic == 1):
            song = song_1
            beat = beat_1
        elif(whichmusic == 2):
            song = song_2
            beat = beat_2
        elif(whichmusic == 3):
            song = song_3
            beat = beat_3
        # Modify the duty cycle to 50 and the frequency will take effect
        self.Buzz.ChangeDutyCycle(50)
        for i in range(0, len(song)):#iterate over all tones   
            if song[i] == 0:# 0 mute
                self.Buzz.ChangeDutyCycle(100)            
            else:# Change the frequency control tone
                self.Buzz.ChangeDutyCycle(50)
                self.Buzz.ChangeFrequency(song[i])
            # Control playback time by beat
            time.sleep(beat[i] * metre) 
        # mute
        self.Buzz.ChangeDutyCycle(100)
        
    def destory(self):
        self.Buzz.stop()					# Stop the buzzer
        #GPIO.output(self.BEPP_PIN, 1)		# Set Buzzer pin to High
        GPIO.cleanup()				# Release resource

