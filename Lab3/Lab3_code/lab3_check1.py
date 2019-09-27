# from machine import Pin, I2C

# # construct an I2C bus
# i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

# i2c.readfrom(0x3a, 4)   # read 4 bytes from slave device with address 0x3a
# i2c.writeto(0x3a, '12') # write '12' to slave device with address 0x3a

# buf = bytearray(10)     # create a buffer with 10 bytes
# i2c.writeto(0x3a, buf)  # write the given buffer to the slave



import machine
import ssd1306
from machine import RTC
from machine import Pin
import time
import sys


## Global Variables
global is_setting_mode
global position
global is_add
global mode
global mode_cur

## There is 3 modes, which is FALSE, ON-ADD, ON-SUB
modes = [(False, False), (True, True), (True, False)]
mode_cur = 0

is_setting_mode = modes[mode_cur][0]
is_add = modes[mode_cur][1]

set_attr_list = ['YEAR', 'MON', 'DAY', 'WEEK', 'HOUR', 'MIN']
position = 0


## Date Variables
big_month = [1, 3, 5, 7, 8, 10, 12]
week_day = ['S', 'M', 'T', 'W', 'R', 'F', 'SA']
init_date = [2019, 1, 1, 0, 0, 0, 0, 0]


## I2C and OLED Initialization
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

## RTC Intializaion
rtc = RTC()
rtc.datetime(tuple(init_date))


## Methods

# def put(x, y, delta_x, delta_y):
# 	oled.fill(0)
# 	if is_setting_mode:
# 		oled.text("ON",0, 0)
# 	else:
# 		oled.text("OFF",0, 0)
# 	oled.text(set_attr_list[position][0].upper(), 120, 0)
# 	oled.text("{0}-{1}{2}-{3}{4}".format(content[0], fill_month, content[1], fill_day, content[2]), x, y)
# 	oled.text("{0}{1}:{2}{3}".format(fill_hour, content[3], fill_minute, content[4]), x + delta_x, y + delta_y)
# 	oled.show()

def buttonAOn(line):
	global is_setting_mode, is_add, mode_cur, modes
	mode_cur += 1
	mode_cur %= 3
	is_setting_mode = modes[mode_cur][0]
	is_add = modes[mode_cur][1]

	if is_setting_mode == False:
		rtc.datetime(tuple(init_date))


def buttonBOn(line):
	global is_setting_mode, position

	if is_setting_mode:
		position += 1
		position %= 6

	time.sleep_ms(500)

def buttonCOn(line):
	global position, is_setting_mode, is_add


	if is_setting_mode == False:
		pass
	else:
		if is_add:

			init_date[position] += 1

			if position == 0:
				pass

			elif position == 1:
				if init_date[position] > 12:
					init_date[position] = 1

			elif position == 2:
				year = init_date[0]
				month = init_date[1]
				if month == 2:
					if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
						if init_date[position] > 29:
							init_date[position] = 1
					else:
						if init_date[position] > 28:
							init_date[position] = 1
				elif month in big_month:
					if init_date[position] > 31:
						init_date[position] = 1
				else:
					if init_date[position] > 30:
						init_date[position] = 1

			elif position == 3:
				if init_date[position] > 7:
					init_date[position] = 0

			elif position == 4:
				if init_date[position] >= 24:
						init_date[position] = 0
			else:
				if init_date[position] >= 60:
						init_date[position] = 0

		else:

			init_date[position] -= 1

			if position == 1 or position == 2:
				if init_date[position] < 1:
					init_date[position] = 1
			else:
				if init_date[position] < 0:
					init_date[position] = 0

	time.sleep_ms(500)





button_A = Pin(0, Pin.IN, Pin.PULL_UP)
# button_B = Pin(16, Pin.IN, Pin.PULL_UP)
button_B = Pin(16, Pin.IN)
button_C = Pin(2, Pin.IN, Pin.PULL_UP)

button_A.irq(handler = buttonAOn, trigger = Pin.IRQ_FALLING)
# button_B.irq(handler = buttonBOn, trigger = Pin.IRQ_FALLING)
button_C.irq(handler = buttonCOn, trigger = Pin.IRQ_FALLING)



while True:
	if button_B.value() == 0:
		buttonBOn(0)

	fill_month = ''
	fill_day = ''
	fill_hour = ''
	fill_minute = ''


	print("----------------------------")
	if is_setting_mode:
		print("UNDER SETTING")
		print("IS ADD?  " + str(is_add))
		print("AD ITEM IS " + str(set_attr_list[position]))
		content = init_date

	else:
		print("OFF SETTING")
		content = rtc.datetime()


	if len(str(content[1])) == 1:
		fill_month = '0'
	if len(str(content[2])) == 1:
		fill_day = '0'
	if len(str(content[4])) == 1:
		fill_hour = '0'
	if len(str(content[5])) == 1:
		fill_minute = '0'


	# print("{0}-{1}{2}-{3}{4}".format(content[0], fill_month, content[1], fill_day, content[2]))
	# print("{0}{1}:{2}{3}:{4}".format(fill_hour, content[3], fill_minute, content[4], content[5]))
	print(content)

	oled.fill(0)
	if is_setting_mode:
		if is_add:
			mod = "ADD"
		else:
			mod = "SUB"
		oled.text("ON - " + mod,0, 0)
		oled.text(set_attr_list[position], 92, 0)
		
	else:
		oled.text("OFF",0, 0)


	text1 = str(content[0]) + '-' + fill_month + str(content[1]) + '-' + fill_day + str(content[2]) + '-' + str(week_day[content[3]])
	text2 = fill_hour + str(content[4]) + ' : ' + fill_minute + str(content[5])
	print(text1)
	print(text2)
	print("----------------------------")

	# oled.text("{0}-{1}{2}-{3}{4}".format(content[0], fill_month, content[1], fill_day, content[2]), 25, 10)
	# oled.text("{0}{1}:{2}{3}".format(fill_hour, content[3], fill_minute, content[4]), 25 + 10, 10 + 15)
	oled.text(text1, 15, 10)
	oled.text(text2, 30, 25)
	oled.show()



