import machine
import socket
import ssd1306
import time
from machine import RTC
from machine import Pin
from machine import ADC
from machine import PWM
import network
import urequests as requests

## I2C and OLED Initialization
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


## Date Variables
global init_date,week_day,request_list, cur_weekd, state
big_month = [1, 3, 5, 7, 8, 10, 12]
week_day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
cur_weekd  = 0
init_date = [2019, 1, 1, 0, 0, 0, 0, 0]
request_list = ['display','off','time']
state = "OFF"


def displayTime(content):
    global cur_weekd
    fill_month = ''
    fill_day = ''
    fill_hour = ''
    fill_minute = ''
    fill_second = ''

    if len(str(content[1])) == 1:
        fill_month = '0'
    if len(str(content[2])) == 1:
        fill_day = '0'
    if len(str(content[4])) == 1:
        fill_hour = '0'
    if len(str(content[5])) == 1:
        fill_minute = '0'
    if len(str(content[6])) == 1:
        fill_second = '0'

    text1 = str(content[0]) + '-' + fill_month + str(content[1]) + '-' + fill_day + str(content[2]) + '-' + str(week_day[cur_weekd])
    text2 = fill_hour + str(content[4]) + ' : ' + fill_minute + str(content[5]) + ' : ' + fill_second + str(content[6])

    oled.fill(0)
    oled.text(text1, 12, 12)
    oled.text(text2, 20, 25)
    oled.show()

def displayStr(content):
    text1 = 'You words are:'
    text2 = content
    oled.fill(0)
    oled.text(text1, 2, 12)
    oled.text(text2, 0, 25)
    oled.show()

## RTC Intializaion
rtc = RTC()
rtc.datetime(tuple(init_date))

sta_if = network.WLAN(network.STA_IF)

def doconnect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def getRealTime():
    global init_date, week_day, cur_weekd
    url_time = "http://worldtimeapi.org/api/timezone/America/New_York"
    r = requests.get(url=url_time)
    NYtime = r.json()
    datetime = NYtime['datetime']
    init_date[0] = int(datetime[0:4])
    init_date[1] = int(datetime[5:7])
    init_date[2] = int(datetime[8:10])
    cur_weekd = int(NYtime['day_of_week'])
    init_date[4] = int(datetime[11:13])
    init_date[5] = int(datetime[14:16])
    rtc.datetime(tuple(init_date))



def respondToAndriod(request):
    global request_list, count, state
    if request not in request_list:
        response = "COMMAND NOT FOUND"
        if state == "ON":
            displayStr(request)
    elif request == 'display':
        response = "GET REQUEST ON"
        state = "ON"
        displayTime(rtc.datetime())
    elif request == 'off':
        response = "GET REQUST OFF"
        state = "OFF"
        oled.fill(0)
        oled.show()
    elif request == 'time':
        response = "GET REQUEST TIME"
        if state == "ON":
            getRealTime()
            displayTime(rtc.datetime())


    return response


doconnect()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
# s.setblocking(0)
s.listen(5)




command = 'off'
while True:

    try:
        s.settimeout(0.9)
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)

        try:
            command = request.split("=")[1].split(' ')[0]
            command = " ".join(command.split("%20"))
        except:
            command = ""

        print(command)
        response = respondToAndriod(command)

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

    except:
        if state == "OFF":
            pass
        elif command == 'time' or command == 'display':

            displayTime(rtc.datetime())

