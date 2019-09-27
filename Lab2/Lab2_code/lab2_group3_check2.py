from machine import PWM
from machine import Pin
from machine import ADC
import time

count = False

def programOn(line):
    global count
    count = not count
    if count == True:
        print('button pushed!')
    else:
        print('button released!')


pin14 = Pin(14,Pin.IN,Pin.PULL_UP)
pin14.irq(handler = programOn, trigger = Pin.IRQ_RISING|Pin.IRQ_FALLING)


while 1:

    pass


