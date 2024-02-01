'''
############################################
rc_ledcontroller V0.1

File:    utils.py
Created: 2024-01-20 I.O.

Info:
Additional utilities 

Status: Beta
############################################
'''

from machine import Timer
from config import sig_move, sig_min, sig_max, sig_dz, sigLevels
from math import sin, sqrt, radians

def calcBreath(PwmMin, PwmMax, PwmRange, bSqrt=False):
    
    print("calc breathing values")
    
    lstBreath=[]
    
    for i in range(PwmMin, PwmMax+1):
        
        if bSqrt:
            fPercent = round(sqrt(i/PwmMax)*PwmRange)
        else:
            fPercentRad=i/PwmMax*180
            fPercent=round(sin(radians(fPercentRad))*PwmRange)
            
        #print(i, fPercent)    
        lstBreath.append([i, fPercent])
        
    print("calc breathing values done")
    
    return lstBreath
            
            
def genSigLevels():
    
    print("calc siglevels")
    
    sigLevels.append([0, sig_min, sig_dz]) #sig_fail
    sigLevels.append([sigLevels[-1][1], sigLevels[-1][1]+sig_dz, sig_dz]) #sig_1
    sigLevels.append([sigLevels[-1][1], sigLevels[-1][1]+sig_dz, sig_dz]) #sig_2
    sigLevels.append([sigLevels[-1][1], sigLevels[-1][1]+sig_dz, sig_dz]) #sig_3
    
    sigLevels.append([int((sig_max + sig_min+90) / 2 - sig_move - sig_dz), int((sig_max + sig_min+90) / 2 + sig_move + sig_dz), sig_dz]) #sig_turn(4)
    
    sigLevels.append([sigLevels[-1][1], sigLevels[-1][1]+sig_dz, sig_dz]) #sig_5
    sigLevels.append([sigLevels[-1][1], sigLevels[-1][1]+sig_dz, sig_dz]) #sig_6
    sigLevels.append([sigLevels[-1][1], sigLevels[-1][1]+sig_dz, sig_dz]) #sig_7
    
    print("calc siglevels done")
    
    return sigLevels
    
    
def checkTimeout(tStart, tLast, timeout):
    return (tStart  - tLast  > timeout or tLast == 0)

