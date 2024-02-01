# rc_ledcontroller

Control PWM LEDs with hobby rc receiver

## Hardware needed:
- flight controller or pwm rx and programmable transmitter
- ESP32 with at least 2 PWM outputs and an analog input
- 2x mosfet (with optocoppler) FR120N, LR7843, AOD4184 working fine
- dinnable LEDs (obviosly), but could be used for all pwm driven electronics

## Wiring:
- following/change config.py for matching pins for the specific board layout
- make sure logic level of fc/rx has 3.3V or use an optocppler

Additional details coming soon (maybe...)
