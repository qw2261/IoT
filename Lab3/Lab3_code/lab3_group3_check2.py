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


## ADC Button
adc0 = ADC(0)

oled.fill(0)
oled.text('HELLO', 0, 0)
oled.show()

while True:

    ## Adjust Lightness Based on Outside Lightness
    oled.contrast((adc0.read() <= 255) * adc0.read() +  (adc0.read() > 255) * 255)


    time.sleep_ms(200)
