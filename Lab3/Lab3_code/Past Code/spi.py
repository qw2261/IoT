import machine
import ssd1306
from machine import RTC
from machine import Pin, SPI, I2C
import ustruct
import time




POWER_CTL = const(0x2D)
DATA_FORMAT = const(0x31)
DATAX0 = const(0x32)
DATAX1 = const(0x33)
DATAY0 = const(0x34)
DATAY1 = const(0x35)
DATAZ0 = const(0x36)
DATAZ1 = const(0x37)




def init_ac():
    writeReg(DATA_FORMAT, 0x01)
    writeReg(POWER_CTL, 0x08)

def writeReg(add, data):
    write_add = ustruct.pack('b', add)
    write_data = ustruct.pack('b', data)

    pincs.off()
    spi.write(write_add)
    spi.write(write_data)
    pincs.on()

def readReg(add):

    add = 0x80 | add
    add = 0x40 | add
    add = ustruct.pack('b', add)

    x1 = bytearray(1)
    x2 = bytearray(1)
    y1 = bytearray(1)
    y2 = bytearray(1)
    z1 = bytearray(1)
    z2 = bytearray(1)

    pincs.off()
    spi.write(add)
    spi.readinto(x1)
    spi.readinto(x2)
    spi.readinto(y1)
    spi.readinto(y2)
    spi.readinto(z1)
    spi.readinto(z2)
    pincs.on()

    x = (ustruct.unpack('b', x2)[0] << 8) | (ustruct.unpack('b', x1)[0])
    y = (ustruct.unpack('b', y2)[0] << 8) | (ustruct.unpack('b', y1)[0])
    z = (ustruct.unpack('b', z2)[0] << 8) | (ustruct.unpack('b', z1)[0])

    return (x, y, z)


i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


pincs = Pin(12, Pin.OUT)
spi = SPI(1, baudrate=5000000, polarity=1, phase=1)

while True:
    x, y, z = readReg(DATAX0)
    print(x ,y ,z)

    time.sleep_ms(200)