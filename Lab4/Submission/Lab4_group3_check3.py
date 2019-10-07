import urequests as requests
import machine
import ssd1306
from machine import RTC
from machine import Pin
from machine import ADC
from machine import PWM
import time
import socket
import network


sta_if = network.WLAN(network.STA_IF)

def do_connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

## Network Connect
do_connect()


## I2C and OLED Initialization
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)






## Operator Button Activation
def buttonAOn(line):
    url_time = "http://worldtimeapi.org/api/timezone/America/New_York"
    r = requests.get(url=url_time)
    NYtime = r.json()
    timestamp = NYtime['unixtime']
    ## Sending Twitter by thinkSpeak API
    tweet_json = {
        'api_key': 'YKW2N4FDNUP32BB8',
        'status': ('Here is the sound from group 3' + str(timestamp))
    }
    requests.post('https://api.thingspeak.com/apps/thingtweet/1/statuses/update', json=tweet_json)
    print("Successful!")


## Operator Button of Watch
button_A = Pin(0, Pin.IN, Pin.PULL_UP)


button_A.irq(handler = buttonAOn, trigger = Pin.IRQ_FALLING)






while True:
    oled.fill(0)
    oled.text('Press A to send Twitter', 0, 0)
    oled.show()
    time.sleep_ms(500)


