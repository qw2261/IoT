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





'''
{'location': {'lat': 40.8027, 'lng': -73.9713}, 'accuracy': 3161.0}
'''

## Location and Weather

url_loc = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyA24afb5VJ2UD1Y0sdfvJU2oouGaWzjnAE"
r = requests.post(url = url_loc, json = {"key":"value"})
location = r.json()
latitude = location['location']['lat']
longitude = location['location']['lng']

url_weather = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=874fd32c716aa4cc9496395a12673597"
r = requests.post(url = url_weather, json = {"key":"value"})
# extract text as json
result = r.json()
descrip = result['weather'][0]['description']
temp = result['main']['temp']
print(descrip)
print(temp)

# url_time = "http://worldtimeapi.org/api/timezone/America/New_York"
# r = requests.get(url = url_time)
# NYtime = r.json()
# timestamp = NYtime['unixtime']


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
    oled.text('LA:' + '{:.1f}'.format(latitude) + ';' + 'LO:' + '{:.1f}'.format(longitude), 0, 0)
    oled.text(str(descrip), 0, 12)
    oled.text('Temp: ' + str(temp - 273.15), 0, 25)
    oled.show()
    time.sleep_ms(500)


