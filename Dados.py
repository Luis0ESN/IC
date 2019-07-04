# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 17:03:40 2019

@author: Carlos Nascimento
"""

class dados:
    '''
    def __init__(self, day, month, year, hour, minute, secund, ms, NP, speed, Temperature, BTOTAL, BETA, TOTAL_PRESSURE, BX, BY, BZ):
        
        self.day = day;
        self.month = month;
        self.year = year;
        self.hour = hour;
        self.minute = minute;
        self.secund = secund;
        self.ms = ms;
        self.NP = NP;
        self.speed = speed;
        self.Temparature = Temperature;
        self.BTOTAL = BTOTAL;
        self.BETA = BETA;
        self.TOTAL_PRESSURE = TOTAL_PRESSURE;
        self.BX = BX;
        self.BY = BY;
        self.BZ = BZ;
    '''
    
    ##
    def setDay(self, day):
        self.day = int(day);
        
    def getDay(self):
        return self.day;
    ##
    
    
    ##
    def setMonth(self, month):
        self.month = int(month);
        
    def getMonth(self):
        return self.month;
    ##
    
    
    ##
    def setYear(self, year):
        self.year = int(year);
        
    def getYear(self):
        return self.year;
    ##
    
    
    ##
    def setHour(self, hour):
        self.hour = int(hour);
        
    def getHour(self):
        return self.hour;
    ##
    
    
    ##
    def setMinute(self, minute):
        self.minute = int(minute);
        
    def getMinute(self):
        return self.minute;
    ##
    
    
    ##
    def setSecund(self, secund):
        self.secund = int(secund);
        
    def getSecund(self):
        return self.secund;
    ##
    
    
    ##
    def setMs(self, ms):
        self.ms = int(ms);
        
    def getMs(self):
        return self.ms;
    ##
    
    
    ##
    def setNP(self, NP):
        if NP == '-1.00000E+30':
            self.NP = float('nan');
            
        else:
            self.NP = float(NP);
        
    def getNP(self):
        return self.NP;
    ##    
    
    ##
    def setSpeed(self, speed):
        if speed == '-1.00000E+30':
            self.speed = float('nan');
            
        else:
            self.speed = float(speed);
            
    def getSpeed(self):
        return self.speed;
    ##
    
    
    ##
    def setTemperature(self, Tempereture):
        if Tempereture == '-1.00000E+30':
            self.Tempareture = float('nan');
            
        else:
            self.Tempareture = float(Tempereture);
        
    def getTemperature(self):
        return self.Tempareture;
    ##
    
    
    ##
    def setBETA(self, BETA):
        if BETA == '-1.00000E+30':
            self.BETA = float('nan');
       
        else:
            self.BETA = float(BETA);
    def getBETA(self):
        return self.BETA;
    ##
    
    
    ##
    def setBTOTAL(self, BTOTAL):
        if BTOTAL == '-1.00000E+30':
            self.BTOTAL = float('nan');
            
        else:
            self.BTOTAL = float(BTOTAL);
    
    def getBTOTAL(self):
        return self.BTOTAL;
    ##   
    
    
    ##
    def setTOTAL_PRESSURE(self, TOTAL_PRESSURE):
        if TOTAL_PRESSURE == '-1.00000E+30':
            self.TOTAL_PRESSURE = float('nan');
        
        else:
            self.TOTAL_PRESSURE = float(TOTAL_PRESSURE);
        
    def getTOTAL_PRESSURE(self):
        return self.TOTAL_PRESSURE;
    ##
    
    
    ##
    def setBX(self, BX):
        if BX == '-1.00000E+30':
            self.BX = float('nan');
        
        else:
            self.BX = float(BX);
        
    def getBX(self):
        return self.BX;
    ##
    
    
    ##
    def setBY(self, BY):
        if BY == '-1.00000E+30':
            self.BY = float('nan');
        
        else:
            self.BY = float(BY);
            
    def getBY(self):
        return self.BY;
    ##
    
    
    ##
    def setBZ(self, BZ):
        if BZ == '-1.00000E+30':
            self.BZ = float('nan');
            
        else:
            self.BZ = float(BZ);
        
    def getBZ(self):
        return self.BZ;
    ##
    
    
    ##
    def imprime(self):
        '''
        print('\n\ndia = {}'.format(self.getDay()))#, end='/')
        print(self.getMonth())#, end='/');
        print(self.getYear());
        print('horario = {}'.format(self.getHour()), end='h ');
        print(self.getMinute(), end='m ');
        print(self.getSecund(), end='s ');
        print('{}ms'.format(self.getMs()));
		'''
		#print('\n\ndia = {}/{}/{} horario = {}h {}m {}s {}ms\nBTOTAL = {}\nNP = {}\nSpeed = {}\nTemperature = {}\nVP RTN = {}\nBETA = {}\nTotal Pressure = {}\nBX = {}\nBY = {}\nBZ = {}'.format(self.getDay(), self.getMonth(), self.getYear(), self.getHour(), self.getMinute(), self.getSecund(), self.getMs(), self.getNP(), self.getSpeed(), self.getTemperature(), self.getVP_RTN(), self.getBETA(), self.getTOTAL_PRESSURE(), self.getBX(), self.getBY(), self.getBZ()));
        print('\n\ndia = {}/{}/{} \nhorario = {}h {}m {}s {}ms\nBTOTAL = {}\nNP = {}\nSpeed = {}\nTemperature = {}\nVP RTN = {}\nBETA = {}\nTotal Pressure = {}\nBx = {}\nBy = {}\nBz = {}\n'.format(self.getDay(), self.getMonth(), self.getYear(), self.getHour(), self.getMinute(), self.getSecund(), self.getMs(), self.getBTOTAL(), self.getNP(), self.getSpeed(), self.getTemperature(), self.getVP_RTN(), self.getBETA(), self.getTOTAL_PRESSURE(), self.getBX(), self.getBY(), self.getBZ()))
    ##