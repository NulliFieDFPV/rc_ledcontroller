'''
############################################
rc_ledcontroller V0.1

File:    ledPort.py
Created: 2024-01-20 I.O.

Info:
PWM Controller Output

Status: Beta
############################################
'''

from time import ticks_ms, ticks_us
from machine import Pin, PWM
from utils import calcBreath

class ledModule(object):
    
    def __init__(self, lstPins, frequency, PwmMin=0, PwmMax=1023):
        self._pins=lstPins
        self._frequency=frequency
        self._leds=[]
        self._PwmMax=PwmMax
        self._PwmMin=PwmMin
        self._ledCount=0
        self._breathUp=False
        self._breathPerc=0
        self._intFlashticks=0
        self._bSqrt=False
        self._lstBreath=[]
        self._lstBIndex=[]
        self._lstBreathPercent=[]
        
        self._initLeds()
    
    @property
    def lastTrigger(self):
        lastT=0
        
        for ledIndex in range(self._ledCount):
            led=self._leds[ledIndex]
            lastT= max(led.lastTrigger, lastT)
            
        return lastT
    
    def lightOff(self, ledIndex=-1):
        
        if ledIndex >=0:
            led=self._leds[ledIndex]
            led.setPwm(led.PwmMin)
        else:    
            for ledIndex in range(self._ledCount):
                led=self._leds[ledIndex]
                led.setPwm(led.PwmMin)
        
        
    def lightOn(self, ledIndex=-1):
        
        if ledIndex >=0:
            led=self._leds[ledIndex]
            led.setPwm(led.PwmMax)
        else:    
            for ledIndex in range(self._ledCount):
                led=self._leds[ledIndex]
                led.setPwm(led.PwmMax)
                
                
    def toggle(self, ledIndex=-1):
        
        if ledIndex >=0:
            led=self._leds[ledIndex]
            bOn= (led.curr< led.PwmMax)
            if bOn:
                led.setPwm(led.PwmMin)
            else:
                led.setPwm(led.PwmMax)
        else:
            ledMaster=self._leds[ledIndex]
            bOn= (ledMaster.curr < ledMaster.PwmMax)
            if bOn:
                ledMaster.setPwm(ledMaster.PwmMax)
            else:
                ledMaster.setPwm(ledMaster.PwmMin)
                
            for ledIndex in range(self._ledCount):
                if ledIndex == ledMaster.ledIndex:
                    continue
                
                led=self._leds[ledIndex]
                bOn= (ledMaster.curr < ledMaster.PwmMax)
                if bOn:
                    led.setPwm(led.PwmMax)
                else:
                    led.setPwm(led.PwmMin)
        
                
    def percent(self, fPercent, ledIndex=0):
        
        if ledIndex >=0:
            led=self._leds[ledIndex]
            led.setPwm(int(led.PwmMin + led.PwmRange*fPercent/100))
        else:    
            for ledIndex in range(self._ledCount):
                led=self._leds[ledIndex]
                led.setPwm(int(led.PwmMin + led.PwmRange*fPercent/100))
                
                
    def doubleflash(self, ledIndex=0):
        
        ledMaster=self._leds[ledIndex]
        
        if self._intFlashticks in [0,3]:
            newPwm=ledMaster.PwmMax
        else:
            newPwm=ledMaster.PwmMin
            
        self._intFlashticks +=1
        
        if self._intFlashticks >20:
            self._intFlashticks=0
            
        for ledIndex in range(self._ledCount):
            led=self._leds[ledIndex]
            led.setPwm(newPwm)
                
    
    def blink(self, ledIndex=0):
        
        ledMaster=self._leds[ledIndex]
        bOn= (ledMaster.curr < ledMaster.PwmMax)
        
        for ledIndex in range(self._ledCount):
            led=self._leds[ledIndex]
            if bOn:
                led.setPwm(led.PwmMax)
            else:
                led.setPwm(led.PwmMin)
            
            
    def breath(self, speed, ledIndex=0):
        ledMaster=self._leds[ledIndex]
        
        if self._breathPerc == ledMaster.PwmMax:
            self._breathUp=False
            #self._breathPerc = 0
        elif self._breathPerc == ledMaster.PwmMin:
            self._breathUp=True
        
        if self._breathUp==True:
            self._breathPerc += speed
        else:
            self._breathPerc -= speed
            
        self._breathPerc = max(ledMaster.PwmMin,min(ledMaster.PwmMax,self._breathPerc))
                    
        #print(self._breathPerc,fPercent)
        breath = (next(c for c in self._lstBreathPercent if c[0] == self._breathPerc))[1]
        newPwm = ledMaster.PwmMin + ledMaster.PwmRange - breath
        
        for ledIndex in range(self._ledCount):
            led=self._leds[ledIndex]
            led.setPwm(newPwm)
                
        
    def _initLeds(self):
        
        for i in range(len(self._pins)):
            led = ledPort(self._pins[i], self._frequency, self._PwmMin, self._PwmMax, self._ledCount )
            self._leds.append(led)
            self._ledCount += 1
            
        ledMaster=self._leds[0]
                
        self._lstBreathPercent = calcBreath(ledMaster.PwmMin, ledMaster.PwmMax+1, ledMaster.PwmRange, self._bSqrt)
 
            
        
        
class ledPort(object):
    def __init__(self, pin, frequency, PwmMin, PwmMax, ledIndex):
        self._pin =pin
        self._frequency =frequency
        self.lastTrigger=0
        self.curr=PwmMin
        self.currPrev=PwmMin
        self.PwmMax=PwmMax
        self.PwmMin=PwmMin
        self.PwmRange=self.PwmMax-self.PwmMin
        self.ledIndex=ledIndex
        self._mosfet=None
        
        self._initMosfet()
    
    
    def setPwm(self, newPwm):
        
        newPwm=min(max(newPwm, self.PwmMin),self.PwmMax)
        
        if newPwm != self.curr:
            self.currPrev=self.curr
            self.curr=newPwm
            #print(newPwm, self.ledIndex)
            self._mosfet.duty(newPwm)
            
        self.lastTrigger=ticks_us()
        
        
    def _initMosfet(self):
        pin_out=Pin(self._pin, Pin.OUT)  # 6 is default onboard lightpin
        self._mosfet= PWM(pin_out, self._frequency)
        
        print("LED " + str(self.ledIndex) + " started")
        
        self.setPwm(self.PwmMin)

        