'''
############################################
rc_ledcontroller V0.1

File:    main.py
Created: 2024-01-20 I.O.

Info:
find Pin and freq config in config.py

Status: Beta
############################################
'''




from machine import Pin, PWM, idle, Timer
from time import ticks_us
from ledPort import ledModule
import ledFu as fu
from utils import checkTimeout, genSigLevels
from config import INPUT_PIN, LIGHT_PIN_1, LIGHT_PIN_2, frequency, period_out, freq_in
from config import sigLevels, arrSigs, pwm_min, pwm_max

ledBoard = ledModule([LIGHT_PIN_1,LIGHT_PIN_2], frequency, pwm_min, pwm_max)
pwm_in = Pin(INPUT_PIN, Pin.IN)

func_is=-1
signal_is=-1
filterSigs=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
bRunning = True

def checkSignal(timer):
    
    global pwm_in, bRunning
    
    try:
        
        sigStart = ticks_us()
        
        while pwm_in.value() == 0:
          if checkTimeout(ticks_us(), sigStart, freq_in*20):
              break
        
        sigStart = ticks_us()
        while pwm_in.value() == 1:
            if checkTimeout(ticks_us(), sigStart, freq_in*20):
              break
        
        sigEnd = ticks_us()

        validateSignal(sigEnd - sigStart)
        
    except KeyboardInterrupt:
        bRunning =False
    
        
def updateLeds(timer):
    
    global func_is, bRunning

    try:
        tick_start= ticks_us()
        
        if func_is ==1:
            fu.fun_1(ledBoard)
                
        elif func_is ==2:
            fu.fun_2(ledBoard)

        elif func_is ==3:
            fu.fun_3(ledBoard, tick_start, 1500000)          
            
        elif func_is ==4:
            fu.fun_4(ledBoard, tick_start, 0, 0, sigLevels[func_is], signal_is)
                
        elif func_is ==5:
            fu.fun_5(ledBoard, tick_start, 50000)
                    
        elif func_is ==6:
            fu.fun_6(ledBoard, tick_start, 50000, 5)
            
        elif func_is ==7:
            fu.fun_7(ledBoard, tick_start, 2000, 5)
            
        elif func_is <=0:
            fu.fun_fs(ledBoard, tick_start, 2000, 5)

    except KeyboardInterrupt:
        bRunning =False            


def validateSignal(signal_in):
    
    global func_is, signal_is, filterSigs
    #signal_in=1440
    func_prod=-1
    signal_is_prod=-1
    iCheck=0
                 
    #print(signal_in)
    for i in range(len(sigLevels)):
        #print(sigLevels[i][0] , signal_in , sigLevels[i][1], i)
        if sigLevels[i][0] < signal_in <= sigLevels[i][1]:
            func_prod=i
            signal_is_prod = signal_in
            break
        
    for i in range(len(arrSigs)):
        if arrSigs[i] == func_prod:
            iCheck +=1
    
    if func_prod > -1:
    
        filterSigs.pop(0)
        filterSigs.append(signal_is_prod)
    
        if filterSigs[0] ==0:
            return
    
        arrSigs.pop(0)
        arrSigs.append(func_prod)
    #print(arrSigs, signal_is_prod, signal_in, iCheck,i, func_prod)

    if iCheck >= i:
        signal_is = int(sum(filterSigs)/len(filterSigs))
        func_is = func_prod
        #print(func_is)


def stopTimer():
    
    timerReader = Timer(0)
    timerReader.deinit()
    timerWriter = Timer(2)
    timerWriter.deinit()
    
def startTimer(inputFreq, outputPeriod):
    
    timerReader = Timer(0)
    timerReader.init(mode=Timer.PERIODIC, freq=inputFreq, callback=checkSignal)
    
    timerWriter = Timer(2)
    timerWriter.init(mode=Timer.PERIODIC, period=outputPeriod, callback=updateLeds)
    
    
def main():
    
    global bRunning
    
    print("starting")
    
    genSigLevels()
    
    startTimer(freq_in, period_out)
    
    print("started")
    
    try:
        while bRunning:
            pass
        
    except KeyboardInterrupt:
        
        bRunning=False
        print('finishing')
        stopTimer()
        print('finished')    

if __name__ == '__main__':
    main()
