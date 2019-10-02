import machine
import ssd1306
from machine import RTC
from machine import Pin
from machine import SPI
import time
import sys

pincs = Pin(12, Pin.OUT)
spi = SPI(1, baudrate=5000000, polarity=0, phase=0)

global buf
buf = bytearray(1)
# def reg_read():
#     pincs.off()
#     spi.write(0x00 & 0x80)
#     print(spi.read(8))
#     # spi.write(0x33 & 0x80)
#     # print(spi.read(8))
#     pincs.on()

def reg_read(reg):
    global buf
    pincs.off()
    spi.readinto(buf, reg)
    spi.readinto(buf)
    pincs.on()
    return buf[0]


# def reg_write_bytes(self, reg, buf):
#     self.cs(0)
#     self.spi.readinto(self.buf, 0x20 | reg)
#     self.spi.write(buf)
#     self.cs(1)
#     return self.buf[0]


def reg_write(reg, value):
    global buf
    pincs.off()
    spi.readinto(buf, 0x80 | reg)
    ret = buf[0]
    spi.readinto(buf, value)
    pincs.on()
    return ret

while True:
    print(reg_read(0x00 | 0x80))
    time.sleep_ms(100)