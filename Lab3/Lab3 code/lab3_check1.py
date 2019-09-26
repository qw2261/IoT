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
global set_attr
global position
global is_add
global prev_time
global counter

is_setting_mode = False
set_attr_list = ['year', 'month', 'day', 'hour', 'minute']
position = 0
set_attr = set_attr_list[position]
is_add = True
prev_time = time.time()

couter = 0


## Date Variables
big_month = [1, 3, 5, 7, 8, 10, 12]
init_date = [2019, 1, 1, 0, 0, 0, 0, 0]


## I2C and OLED Initialization
i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

## RTC Intializaion
rtc = RTC()
rtc.datetime(tuple(init_date))


def buttonAOn():
	global is_setting_mode
	is_setting_mode = not is_setting_mode
	if is_setting_mode == False:
		rtc.datetime(tuple(init_date))


def buttonBOn():
	global is_setting_mode, position

	if is_setting_mode:
		position += 1
		position %= 5
		set_attr = set_attr_list[position]

def buttonCOn():
	global prev_time, position, is_setting_mode, counter

	counter += 1

	if not is_setting_mode:
		counter = 0
		return


	if counter % 2 != 0:
		prev_time = time.time()

	elif time.time() - prev_time >= 2:
			is_add = not is_add
			return
			
	else:
		if is_add:
			init_date[position] += 1

			if position == 0:
				pass
			elif position == 1:
				if init_date[position] > 12:
					init_date[position] = 1
			elif position == 2:
				if init_date[1] == 2:
					if (init_date[0] % 4 == 0 and init_date[0] % 100 != 0) or (init_date[0] % 400 == 0):
						if init_date[position] > 29:
							init_date[position] = 1
					else:
						if init_date[position] > 28:
							init_date[position] = 1
				elif init_date[1] in big_month:
					if init_date[position] > 31:
						init_date[position] = 1
				else:
					if init_date[position] > 30:
						init_date[position] = 1

			elif position == 3:
				if init_date[position] >= 24:
						init_date[position] = 0
			else:
				if init_date[position] >= 60:
						init_date[position] = 0
		else:
			init_date[position] -= 1

			if position == 0:
				if init_date[position] < 0:
					init_date[position] = 0

			elif position == 1:
				if init_date[position] <= 0:
					init_date[position] = 12

			elif position == 2:
				if init_date[position] <= 0:
					if init_date[1] == 2:
						if (init_date[0] % 4 == 0 and init_date[0] % 100 != 0) or (init_date[0] % 400 == 0):
							init_date[position] = 29
						else:
							init_date[position] = 28
					elif init_date[1] in big_month:
						init_date[position] = 31
					else:
						init_date[position] = 30

			elif position == 3:
				if init_date[position] < 0:
						init_date[position] = 23
			else:
				if init_date[position] < 0:
						init_date[position] = 59






button_A = Pin(0, Pin.IN, Pin.PULL_UP)
button_B = Pin(16, Pin.IN, Pin.PULL_UP)
button_C = Pin(2, Pin.IN, Pin.PULL_UP)

button_A.irq(handler = buttonAOn, trigger = Pin.IRQ_FALLING)
button_B.irq(handler = buttonBOn, trigger = Pin.IRQ_FALLING)
button_C.irq(handler = buttonCOn, trigger = Pin.IRQ_FALLING|Pin.IRQ_RISING)



while True:
	fill_hour = ''
	fill_minute = ''

	oled.fill(0)
	cur = rtc.datetime()
	if len(str(cur[3])) == 1:
		fill_hour = '0'
	if len(str(cur[4])) == 1:
		fill_minute = '0'

	oled.text("{0}-{1}-{2} {3}{4}:{5}{6}".format(cur[0], cur[1], cur[2], fill_hour, cur[3], fill_minute, cur[4]), 10, 20)
	oled.show()

