#!/usr/bin/python
# -*- coding:utf-8 -*-

# from . import I2C_config
import time
# from . import I2C_config
import smbus

Seconds_Reg = 0x00
Min_Reg     = 0x01
Hour_Reg    = 0x02
Day_Reg     = 0x03
Date_Reg    = 0x04
Month_Reg   = 0x05
Year_Reg    = 0x06

class DS3231:
    def __init__(self,add = 0x68):
        self.i2c = smbus.SMBus(1)
        self.address = add#0x20   
        
    def Read_Reg(self, Reg):
        return self.i2c.read_byte_data (self.address, Reg)
        
    def Write_Reg(self, Reg, data):
        self.i2c.write_byte_data(self.address, Reg, data)
        
    def BCD_Convert_DEC(self, code):
        code1 =(((code & 0xf000)>>12) )*1000  + (((code & 0xf00)>>8) )*100  + (((code & 0xf0)>>4) )*10  + (code & 0x0f)
        return code1;
    
    def DEC_Convert_BCD(self, code):
        code1 = code%10 + ((int(code/10)%10) << 4) + ((int(code/100)%10) << 8) + ((int(code/1000)%10) << 12)
        return int(code1);
    
    """
        The year can only be from 0 to 99, and Century can be 0 or 1, depending on how you express it.
        If the 21st century is considered to be 1, then the year represented is from 1900 to 2099.
        If the 21st world is considered to be 0, it means that the year is from 2000 to 2199.
    """
    #I have calculated from 2000 here, and it is 0 in the 21st century
    
    
    def SET_Calendar(self,Year,Month,Date):
        self.SET_Year_BCD(self.DEC_Convert_BCD(Year))
        self.SET_Month_BCD(self.DEC_Convert_BCD(Month))
        self.SET_Date_BCD(self.DEC_Convert_BCD(Date))
    
    def Read_Calendar(self):
        Calendar = [0,0,0]
        Calendar[0] = self.BCD_Convert_DEC(self.Read_Year_BCD())
        Calendar[1] = self.BCD_Convert_DEC(self.Read_Month_BCD())
        Calendar[2] = self.BCD_Convert_DEC(self.Read_Date_BCD())
        return Calendar
        
    '''Year_Reg     0x06                            '''
    def Read_Year_BCD(self):
        vai = self.Read_Reg(Month_Reg) & 0x80
        if(vai == 0x80):
            return self.Read_Reg(Year_Reg) | (0x21 << 8)
        else :
            return self.Read_Reg(Year_Reg) | (0x20 << 8)
        
        
    def SET_Year_BCD(self, Year):
        if(Year>=0x2100):
            self.Write_Reg(Year_Reg, Year&0xff)
            
            vai = self.Read_Reg(Month_Reg)
            self.Write_Reg(Month_Reg,  vai | 0x80)
        elif(Year < 0x2100):
            self.Write_Reg(Year_Reg, Year & 0xff)
            
            vai = self.Read_Reg(Month_Reg)
            self.Write_Reg(Month_Reg,  vai & 0x7f)
    
    '''Month_Reg     0x05                            '''
    def Read_Month_BCD(self):
        return self.Read_Reg(Month_Reg)&0x1f
        
    def SET_Month_BCD(self, Month):
        vai = self.Read_Reg(Month_Reg)
        self.Write_Reg(Month_Reg, (vai & 0x80) | Month)
    
    '''Date_Reg     0x04                            '''
    def Read_Date_BCD(self):
        return self.Read_Reg(Date_Reg)&0x3f
        
    def SET_Date_BCD(self, Date):
        self.Write_Reg(Date_Reg, Date&0x3f)
        
    
    '''Day          0x03                            '''
    def Read_Day(self):
        return self.Read_Reg(Day_Reg)&0x07
    
    def Read_Day_str(self):
        vai = self.Read_Reg(Day_Reg)&0x07
        str1  =["SUN","Mon","Tues","Wed","Thur","Fri","Sat"]
        return str1[vai-1]
    
    def SET_Day(self, vai):
        str1  =["SUN","Mon","Tues","Wed","Thur","Fri","Sat"]
        if(vai <= 7):
            self.Write_Reg(Day_Reg, vai&0x07)
        else :
            for i in range(1, 8):
                if(vai == str1[i-1]):
                    self.Write_Reg(Day_Reg, i)
    
    '''Hour         0x02                            '''
    def SET_Time_Hour_BCD(self, data):#
        vai = self.Read_Hour_Mode()
        if(vai == "24"):
            self.Write_Reg(Hour_Reg, data & 0x3F) 
        elif(vai == "AM" or vai == "PM"):
            if(data>0x12):
                data = data-0x12
            self.Write_Reg(Hour_Reg, data & 0x3F) 

    
    
    def SET_Hour_Mode(self, data):#
        vai = self.Read_Reg(Hour_Reg)
        if(data == "12" or data == 12):
            self.Write_Reg(Hour_Reg, vai|0x40) #12 hour
        elif(data == "24" or data == 24 ):
            self.Write_Reg(Hour_Reg, vai&0x3f) #24 hour   
        else:
            print ("Only supports 12 and 24")
            self.Write_Reg(Hour_Reg, vai&0x3f) #24 hour    
    
    def Read_Hour_Mode(self):#
        vai = self.Read_Reg(Hour_Reg)
        if(vai&0x40 == 0x40):#12 hour
            if(vai&0x20 == 0x20):
                return "PM"
            else :
                return "AM"
        else:#24 hour
            return "24"

    def Read_Time_Hour_BCD (self):#
        vai = self.Read_Hour_Mode()
        if(vai == "24"):
            return self.Read_Reg(Hour_Reg) & 0x3F
        elif(vai == "AM" or vai == "PM"):
            vai = self.Read_Reg(Hour_Reg) & 0x1F
            if(vai>0x12):
                vai = vai-0x12
            return vai

    '''Min            0x01                               '''
    def SET_Time_Min_BCD (self, data):
        self.Write_Reg(Min_Reg, data & 0x7F)
        
    def Read_Time_Min_BCD (self):
        return self.Read_Reg(Min_Reg)&0x7F

    '''Sec            0x00                               '''
    def SET_Time_Sec_BCD (self, data):
        self.Write_Reg(Seconds_Reg,data & 0x7F)
    
    def Read_Time_Sec_BCD(self):
        return self.Read_Reg(Seconds_Reg)&0x7F

    '''Time          0x02  01  00                        '''
    def SET_Time(self, Hour, Min, Sec):#
        Hour = self.DEC_Convert_BCD(Hour)
        Min = self.DEC_Convert_BCD(Min)
        Sec = self.DEC_Convert_BCD(Sec)
        
        self.SET_Time_Sec_BCD(Sec&0x7F)
        self.SET_Time_Min_BCD(Min&0x7F)
        self.SET_Time_Hour_BCD(Hour&0x3F)
    
    def Set_Time_BCD(self, Time):
        for i in range(0, 7):
            self.Write_Reg(i,Time[i]);
            
    def Read_Time(self):
        Time = [0,0,0]
        Time[0] = self.BCD_Convert_DEC(self.Read_Time_Hour_BCD())
        Time[1] = self.BCD_Convert_DEC(self.Read_Time_Min_BCD())
        Time[2] = self.BCD_Convert_DEC(self.Read_Time_Sec_BCD())
        return Time
            
            
    '''Read_Temperature      0x11 12                      '''
    def Read_Temperature(self):
        vai = self.Read_Reg(0x0e)
        self.Write_Reg(0x0e, vai|0x20)#Activate temperature conversion
        time.sleep(0.01)   #Wait for temperature conversion
        vai_H = self.Read_Reg(0x11)
        vai_L = self.Read_Reg(0x12)>>6
        return vai_H+vai_L*0.25 #Precision 0.25 Celsius

        
        
if __name__=="__main__":
    str1  =["SUN","Mon","Tues","Wed","Thur","Fri","Sat"]
    RTC = DS3231(add = 0x68)
    
    RTC.SET_Hour_Mode(24)
    RTC.SET_Time(23,59,50)
    RTC.SET_Day(7)  #RTC.SET_Day("Sat")
    RTC.SET_Calendar(2099,12,31)
    while(1):
        time.sleep(1)
        print("Day %s"%RTC.Read_Day_str())
        print (RTC.Read_Calendar())
        Time = RTC.Read_Time()
        print("hour : %d : %d : %d "%(Time[0],Time[1],Time[2]))
        print("hour : %x : %x : %x "%(RTC.Read_Time_Hour_BCD(),RTC.Read_Time_Min_BCD(),RTC.Read_Time_Sec_BCD()))
        print("temperature : %0.2f Celsius"%RTC.Read_Temperature())
        
        