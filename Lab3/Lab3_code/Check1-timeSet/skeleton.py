import machine
import ssd1306
from machine import RTC
from machine import Pin
import time
import sys

## Date Variables
big_month = [1, 3, 5, 7, 8, 10, 12]
week_day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
init_date = [2019, 1, 1, 0, 0, 0, 0, 0]


## I2C and OLED Initialization
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

## RTC Intializaion
rtc = RTC()
rtc.datetime(tuple(init_date))

global button, state, set_mode, modes_size

button = 'NULL'
state = 'HOME'
modes = ['SET_TIME', 'SET_ALARM', 'EXIT']
modes_size = len(modes)
set_mode = 0


## Set Time Variables
global set_time_mode
time_modes = ['YEAR[1]', 'YEAR[2]', 'YEAR[3]', 'YEAR[4]', 'MONTH', 'DAY', 'WEEKDAY', 'HOUR', 'MIN']
set_time_mode = 0
time_modes_size = len(time_modes)

def display(content, Page, Mark):

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

    text1 = str(content[0]) + '-' + fill_month + str(content[1]) + '-' + fill_day + str(content[2]) + '-' + str(week_day[content[3]])
    text2 = fill_hour + str(content[4]) + ' : ' + fill_minute + str(content[5]) + ' : ' + fill_second + str(content[6])

    if len(Mark) >= 7:
        position_mark = 70
    elif len(Mark) == 6:
        position_mark = 75
    elif len(Mark) == 5:
        position_mark = 80
    elif len(Mark) == 4:
        position_mark = 88
    else:
        position_mark = 92

    oled.fill(0)
    oled.text(Page, 0, 0)
    oled.text(Mark, position_mark, 0)
    oled.text(text1, 12, 12)
    oled.text(text2, 20, 25)
    oled.show()


def homeTransition():
    global button, state
    if button == 'A':
        state = 'SELECT'
    else:
        display(rtc.datetime(), 'HOME', '')
    button = 'NULL'

def selectTransition():
    global button, set_mode, modes_size, state
    
    if button == 'A':
        if set_mode == 0:
            state = 'SET_TIME'
        elif set_mode == 1:
            state = 'SET_ALARM'
        else:
            state = 'HOME'
    elif button == 'B':
        set_mode += 1
        set_mode %= modes_size
    elif button == 'C':
        set_mode -= 1
        set_mode %= modes_size

    oled.fill(0)
    oled.text('Menu', 0, 0)
    oled.text(modes[set_mode], 45, 15)
    oled.show()

    button = 'NULL'

def setTime():
    global button, set_time_mode, init_date, time_modes_size, time_modes, state

    if button == 'C':
        rtc.datetime(tuple(init_date))
        state = 'SELECT'

    elif button == 'A':
        set_time_mode += 1
        set_time_mode %= time_modes_size

    elif button == 'B':
        if set_time_mode <= 3 and set_time_mode >= 0:
            year = str(init_date[0])
            if len(year) < 4:
                year = '0' * (4 - len(year)) + year

            year_int = int(year[set_time_mode])
            year_int += 1

            if year_int >= 10:
                year = list(year)
                year[set_time_mode] = '0'
                year = ''.join(year)
            else:
                year = list(year)
                year[set_time_mode] = str(year_int)
                year = ''.join(year)

            init_date[0] = int(year)

        elif set_time_mode == 4:
            init_date[1] += 1
            if init_date[1] > 12:
                init_date[1] = 1

        elif set_time_mode == 5:
            init_date[2] += 1
            year = init_date[0]
            month = init_date[1]

            if month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    if init_date[2] > 29:
                        init_date[2] = 1
                else:
                    if init_date[2] > 28:
                        init_date[2] = 1
            elif month in big_month:
                if init_date[2] > 31:
                    init_date[2] = 1
            else:
                if init_date[2] > 30:
                    init_date[2] = 1

        elif set_time_mode == 6:
            init_date[3] += 1
            if init_date[3] >= 7:
                init_date[3] = 0

        elif set_time_mode == 7:
            init_date[4] += 1
            if init_date[4] >= 24:
                init_date[4] = 0

        else:
            init_date[5] += 1
            if init_date[5] >= 60:
                init_date[5] = 0

    display(init_date, 'TIME', time_modes[set_time_mode])

    button = 'NULL'




def setAlarm():
    global state, button
    state = 'SELECT'
    button = 'NULL'
    pass


def transion():
    global state
    if state == 'HOME':
        homeTransition()
    elif state == 'SELECT':
        selectTransition()
    elif state == 'SET_TIME':
        setTime()
    elif state == 'SET_ALARM':
        setAlarm()



def buttonAOn(line):
    global button
    button = 'A'

def buttonBOn(line):
    global button
    button = 'B'

def buttonCOn(line):
    global button
    button = 'C'





button_A = Pin(0, Pin.IN, Pin.PULL_UP)
button_B = Pin(14, Pin.IN, Pin.PULL_UP)
# button_B = Pin(16, Pin.IN)
button_C = Pin(2, Pin.IN, Pin.PULL_UP)

button_A.irq(handler = buttonAOn, trigger = Pin.IRQ_FALLING)
button_B.irq(handler = buttonBOn, trigger = Pin.IRQ_FALLING)
button_C.irq(handler = buttonCOn, trigger = Pin.IRQ_FALLING)


while True:
    print(button, state)
    # if button_B.value() == 0:
#        buttonBOn(0)
    transion()
    time.sleep_ms(200)
