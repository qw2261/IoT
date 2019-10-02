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

position_x = 0
position_y = 22
oled.fill(0)
oled.text('I LOVE IoT', position, 10)
oled.show()
time.sleep_ms(1000)

while True:
    oled.fill(0)
    oled.text('I LOVE IoT', position_x, position_y)
    print(position)
    position += 7
    if position > 200:
        position = - 70
    oled.show()
    time.sleep_ms(200)
