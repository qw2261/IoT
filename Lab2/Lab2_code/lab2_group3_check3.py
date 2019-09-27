from machine import PWM
from machine import Pin
from machine import ADC
import time

count = 0
record = 1

def ADCprinter(adc):

    time.sleep_ms(100)
   # print(adc.read())
    return adc.read()

def programOn(line):
    global count
    count += 1


class pwm_led():

    def __init__(self, pin, freq=1000):

        self.pwm = PWM(pin,freq=freq)

    def change_duty(self, duty):

        if 0 <= duty and duty <= 1023:
            self.pwm.duty(duty)
        else:
            print('pwm [0-1023] ')

    def deinit(self):
        self.pwm.deinit()



pin2 = Pin(2,Pin.OUT)
pin12 = Pin(12,Pin.OUT)
pin14 = Pin(14,Pin.IN,Pin.PULL_UP)
pin14.irq(handler = programOn, trigger = Pin.IRQ_RISING|Pin.IRQ_FALLING)

pwm2 = pwm_led(pin2)
pwm12 = pwm_led(pin12)

adc0 = ADC(0)

while 1:

    if count%2:
        record = ADCprinter(adc0)
        print(count, record)

    if record > 1020:
        record = 1020
    elif record < 1:
        record = 1

    pwm2.change_duty(int(1022-record))
    pwm12.change_duty(int(record))
