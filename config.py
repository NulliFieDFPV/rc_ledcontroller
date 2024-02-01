'''
############################################
rc_ledcontroller V0.1

File:    config.py
Created: 2024-01-20 I.O.

Info:
configures ports, ranges and frequencies

Status: Beta
############################################
'''

sig_move=220
sig_min=1000
sig_max=2000
sig_dz=60
sigLevels=[]

pwm_min=0
pwm_max=1023

INPUT_PIN = 4
LIGHT_PIN_1 = 20
LIGHT_PIN_2 = 10

frequency = 5000
freq_in = 333
period_out = 10

arrSigs=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
