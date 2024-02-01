'''
############################################
rc_ledcontroller V0.1

File:    ledFu.py
Created: 2024-01-20 I.O.

Info:
PWM patterns for output

Status: Beta
############################################
'''
from utils import checkTimeout

# All functions do have the same parameters, but not all of them needed in each one
# patterns could easily be swapped in main.py to differenz siglevens

def fun_1(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):
    led.lightOff()

def fun_2(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):
    led.lightOn()
    
def fun_3(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):
    if checkTimeout(start, led.lastTrigger, timeout):
        led.toggle()
        
def fun_4(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):

    if sigRange is None:
        return
    
    sig_center=int((sigRange[1]+sigRange[0])/2)
    sig_move = sig_center - sigRange[0] - sigRange[2]
    sig_move_start_l=sig_center - sigRange[2]
    sig_move_start_r=sig_center + sigRange[2]
    
    #print(sig_center, sig_move)
    
    if sig_move_start_l <= signal_is <= sig_move_start_r:
        led.lightOn()
    else:
        if sig_move_start_l > signal_is:
            #left
            newDuty=100-int((sig_move_start_l-signal_is)/sig_move*100)
            #print("l",newDuty)
            led.percent(newDuty, 0)
            led.lightOn(1)
        else:
            newDuty=100-int((signal_is-sig_move_start_r)/sig_move*100)
            #right
            #print("r",newDuty, sig_move_start_l,signal_is,sig_move, sig_move_start_r)
            led.percent(newDuty,1)
            led.lightOn(0)
            
            
def fun_5(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):
    if checkTimeout(start, led.lastTrigger, timeout):
        led.doubleflash()

def fun_6(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):
    if checkTimeout(start, led.lastTrigger, timeout):
        led.doubleflash()
        
def fun_7(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):
    if checkTimeout(start, led.lastTrigger, timeout):
        led.breath(speed)
        
def fun_fs(led, start=0, timeout=50000, speed=5, sigRange=None, signal_is=0):
    if checkTimeout(start, led.lastTrigger, timeout):
        led.breath(5)
        #ledBoard.doubleflash()
        #ledBoard.blink()
        #ledBoard.toggle()
