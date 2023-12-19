from rpi_ws281x import Adafruit_NeoPixel, Color
import random
import time

class WS2812:
    def __init__(self):
        LED_COUNT      = 6      # Number of LED pixels.
        LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
        LED_BRIGHTNESS = 100    # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()
        
    def SetRGB(self, color):        
        print("WS2812 Set RGB")
        print(color)
        # for x in range(0,5):
        for i in range(0, 6):
            self.strip.setPixelColor(i, Color(color[i][0],color[i][1],color[i][2]))	
            self.strip.show()
            # time.sleep(0.1)
            
    def SetPixelColor(self, i, color):
        self.strip.setPixelColor(i, Color(color[0],color[1],color[2]))	
        self.strip.show()
    
    def Close(self):
        for i in range(0, 6):
            self.strip.setPixelColor(i,Color(0 , 0, 0))	
            self.strip.show()