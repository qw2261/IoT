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


## Location and Weather

url_loc = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyA24afb5VJ2UD1Y0sdfvJU2oouGaWzjnAE"
r = requests.post(url = url_loc, json = {"key":"value"})
location = r.json()
latitude = location['location']['lat']
longitude = location['location']['lng']






while True:
    oled.fill(0)
    oled.text('LA:' + '{:.1f}'.format(latitude) + ';' + 'LO:' + '{:.1f}'.format(longitude), 0, 0)
    oled.show()
    time.sleep_ms(500)


