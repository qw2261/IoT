import machine
import ssd1306
from machine import RTC
from machine import Pin
from machine import ADC
from machine import PWM
import time




## I2C and OLED Initialization
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


## Date Variables
big_month = [1, 3, 5, 7, 8, 10, 12]
week_day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
init_date = [2019, 1, 1, 0, 0, 0, 0, 0]


## RTC Intializaion
rtc = RTC()
rtc.datetime(tuple(init_date))

global button, state, set_mode, modes_size

button = 'NULL'
state = 'HOME'
modes = ['SET_TIME', 'SET_ALARM', 'EXIT']
modes_size = len(modes)
set_mode = 0


## Display Settings

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


## Set Time Variables
global set_time_mode
time_modes = ['YEAR[1]', 'YEAR[2]', 'YEAR[3]', 'YEAR[4]', 'MONTH', 'DAY', 'WEEKDAY', 'HOUR', 'MIN']
set_time_mode = 0
time_modes_size = len(time_modes)

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

## Set Alarm Variables
global alarm_state, set_alarm_mode, set_alarm_mode_state, alarms, alarm_cur, alarm_time_cur, alarm_weekday_cur

alarm_states = ['SELECT_ALARM', 'SET_ALARM', 'EXIT']
alarm_state = 'ALARM_HOME'

alarm_set_modes = ['SET_ALARM_TIME', 'SET_ALARM_DAY', 'SAVE_ALARM', 'EXIT']
alarm_set_mode_size = len(alarm_set_modes)
set_alarm_mode = 0
set_alarm_mode_state = 'FUNC_SELECT'

alarm_time_set = ['HOUR', 'MIN']
alarm_time_cur = 0

alarm_weekday_set = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
alarm_weekday_cur = 0

alarms = [[0, 0, [False, False, False, False, False, False, False], False],
          [0, 0, [False, False, False, False, False, False, False], False],
          [0, 0, [False, False, False, False, False, False, False], False]]
alarm_cur = 0


def funcSelectTransition():
    global button, set_alarm_mode_state, alarm_state, set_alarm_mode
    if button == 'A':
        if set_alarm_mode == 0:
            set_alarm_mode_state = 'SET_ALARM_TIME'
        elif set_alarm_mode == 1:
            set_alarm_mode_state = 'SET_ALARM_DAY'
        elif set_alarm_mode == 2:
            set_alarm_mode_state = 'SAVE_ALARM'
        elif set_alarm_mode == 3:
            set_alarm_mode_state = 'FUNC_SELECT'
            alarm_state = 'SELECT_ALARM'

    elif button == 'B':
        set_alarm_mode += 1
        set_alarm_mode %= alarm_set_mode_size
    elif button == 'C':
        set_alarm_mode -= 1
        set_alarm_mode %= alarm_set_mode_size


    oled.fill(0)
    oled.text('FUNCTION SELECT', 0, 0)
    oled.text(' '.join(alarm_set_modes[set_alarm_mode].split('_')), 12, 25)
    oled.show()

    button = 'NULL'

def setAlarmTimeTransition():
    global button, set_alarm_mode_state, alarm_time_cur, alarms, alarm_cur
    if button == 'C':
        set_alarm_mode_state = 'FUNC_SELECT'
    elif button == 'A':
        alarm_time_cur += 1
        alarm_time_cur %= 2
    elif button == 'B':
        if alarm_time_cur == 0:
            alarms[alarm_cur][alarm_time_cur] += 1
            if alarms[alarm_cur][alarm_time_cur] >= 24:
                alarms[alarm_cur][alarm_time_cur] = 0
        elif alarm_time_cur == 1:
            alarms[alarm_cur][alarm_time_cur] += 1
            if alarms[alarm_cur][alarm_time_cur] >= 60:
                alarms[alarm_cur][alarm_time_cur] = 0


    fill_hour = ''
    fill_minute = ''

    if len(str(alarms[alarm_cur][0])) == 1:
        fill_hour = '0'
    if len(str(alarms[alarm_cur][1])) == 1:
        fill_minute = '0'


    oled.fill(0)
    oled.text('SET TIME', 0, 0)
    oled.text(alarm_time_set[alarm_time_cur], 88, 0)
    oled.text(fill_hour + str(alarms[alarm_cur][0]) + ' : ' + fill_minute + str(alarms[alarm_cur][1]), 20, 25)
    oled.show()

    button = 'NULL'


def setAlarmDayTransition():
    global button, set_alarm_mode_state, alarms, alarm_cur, alarm_weekday_cur
    if button == 'C':
        set_alarm_mode_state = 'FUNC_SELECT'
    elif button == 'A':
        alarm_weekday_cur += 1
        alarm_weekday_cur %= 7
    elif button == 'B':
        alarms[alarm_cur][2][alarm_weekday_cur] = not alarms[alarm_cur][2][alarm_weekday_cur]

    on_off_info = 'OFF'
    if alarms[alarm_cur][2][alarm_weekday_cur]:
        on_off_info = 'ON'
    oled.fill(0)
    oled.text('SET DAY', 0, 0)
    oled.text(alarm_weekday_set[alarm_weekday_cur] + ' : ' + on_off_info, 20, 25)
    oled.show()

    button = 'NULL'

def saveAlarmTransition():
    global button, alarms, alarm_cur, set_alarm_mode_state
    if button == 'C':
        set_alarm_mode_state = 'FUNC_SELECT'
    elif button == 'B':
        alarms[alarm_cur][3] = not alarms[alarm_cur][3]

    on_off_info = 'OFF'
    if alarms[alarm_cur][3]:
        on_off_info = 'ON'

    oled.fill(0)
    oled.text('SAVE', 0, 0)
    oled.text('NO.' + str(alarm_cur + 1) + ' : ' + on_off_info, 15, 25)
    oled.show()

    button = 'NULL'

def alarmSetTransition():
    global set_alarm_mode_state
    if set_alarm_mode_state == 'FUNC_SELECT':
        funcSelectTransition()
    elif set_alarm_mode_state == 'SET_ALARM_TIME':
        setAlarmTimeTransition()
    elif set_alarm_mode_state == 'SET_ALARM_DAY':
        setAlarmDayTransition()
    elif set_alarm_mode_state == 'SAVE_ALARM':
        saveAlarmTransition()


def alarmSelectTransition():
    global button, alarm_cur, alarm_state
    if button == 'A':
        alarm_state = 'SET_ALARM'
    elif button == 'B':
        alarm_cur += 1
        alarm_cur %= 3
    elif button == 'C':
        alarm_state = 'ALARM_HOME'
        alarm_cur = 0

    # Display
    oled.fill(0)
    oled.text('SELECT ALARM', 0, 0)
    oled.text('NO.' + str(alarm_cur + 1) + ' SELECTED', 15, 25)
    oled.show()

    button = 'NULL'


def alarmHomeTransition():
    global button, state, alarm_state
    if button == 'A':
        alarm_state = 'SELECT_ALARM'
    elif button == 'C':
        state = 'SELECT'

    count = 0
    on_list = []
    for i, each in enumerate(alarms):
        if each[3]:
            count += 1
            on_list.append(str(i + 1))

    # Display
    oled.fill(0)
    oled.text('ALARM HOME', 0, 0)
    oled.text(str(count) + ' ALARMS WORK', 15, 12)
    oled.text('ON LIST: ' + ','.join(on_list), 15, 25)
    oled.show()

    button = 'NULL'


def setAlarmTransition():
    global alarm_state, state
    if alarm_state == 'ALARM_HOME':
        alarmHomeTransition()
    elif alarm_state == 'SELECT_ALARM':
        alarmSelectTransition()
    elif alarm_state == 'SET_ALARM':
        alarmSetTransition()
    elif alarm_state == 'EXIT':
        state = 'SELECT'
        alarm_state = 'ALARM_HOME'




## Basics

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
    oled.text(' '.join(modes[set_mode].split('_')), 45, 15)
    oled.show()

    button = 'NULL'


def transion():
    global state
    if state == 'HOME':
        homeTransition()
    elif state == 'SELECT':
        selectTransition()
    elif state == 'SET_TIME':
        setTime()
    elif state == 'SET_ALARM':
        setAlarmTransition()

## Alarm Ring to work
def checkTimeMatch(hour_to_match, minute_to_match, weekday_to_match):
    current = rtc.datetime()
    if weekday_to_match[current[3]] and hour_to_match == current[4] and minute_to_match == current[5]:
        return True
    return False

pin12 = Pin(12, Pin.OUT)
def ringDetect():
    global alarms
    for each in alarms:
        if each[3]:
            pwm = PWM(pin12, 1000)
            if checkTimeMatch(each[0], each[1], each[2]):
                pwm.duty(100)
                oled.fill(1)
                oled.show()
                time.sleep_ms(500)
                oled.fill(0)
                oled.show()
                print('Ring Now')
                return True
            else:
                pwm.deinit()





## Operator Button Activation
def buttonAOn(line):
    global button
    button = 'A'


def buttonBOn(line):
    global button
    button = 'B'


def buttonCOn(line):
    global button
    button = 'C'



## Operator Button of Watch
button_A = Pin(0, Pin.IN, Pin.PULL_UP)
button_B = Pin(3, Pin.IN, Pin.PULL_UP)
button_C = Pin(2, Pin.IN, Pin.PULL_UP)

button_A.irq(handler = buttonAOn, trigger = Pin.IRQ_FALLING)
button_B.irq(handler = buttonBOn, trigger = Pin.IRQ_FALLING)
button_C.irq(handler = buttonCOn, trigger = Pin.IRQ_FALLING)

## ADC Button
adc0 = ADC(0)



while True:
    print(button, state)
    print(rtc.datetime())
    print(alarms[0])
    print(alarms[1])
    print(alarms[2])

    ringDetect()
    print('---------------')

    ## Adjust Lightness Based on Outside Lightness
    oled.contrast((adc0.read() <= 255) * adc0.read() +  (adc0.read() > 255) * 255)

    ## Watch Function Transitions
    transion()

    time.sleep_ms(200)
