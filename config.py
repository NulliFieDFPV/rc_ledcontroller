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


sig_move=220                              # Range for turn signaling in microseconds
sig_min=1000                              # Min PWM allowed in microseconds
sig_max=2000                              # Max PWM allowed in microseconds
sig_dz=60                                 # Deadzone for signal in microseconds
sigLevels=[]                              # Public List of signals generated for PWM in, check utils.py

pwm_min=0                                 # Min PWM for PWM output/leds in microseconds
pwm_max=1023                              # Max PWM for PWM output/leds in microseconds

INPUT_PIN = 4                             # Input Pin for signal from rx/fc
LIGHT_PIN_1 = 20                          # Output Pin 1 for LED
LIGHT_PIN_2 = 10                          # Output Pin 2 for LED
#LIGHT_PIN_3 = 10                          # Output Pin 3 for LED

frequency = 5000                          # PWM frequency for output
freq_in = 333                             # frequency for input timer
period_out = 10                           # period for output timer

arrSigs=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   # Shifting array for signal verification
