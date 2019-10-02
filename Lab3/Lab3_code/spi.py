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

def readReg():

    add = 0x80 | DATAX0
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


pincs = Pin(15, Pin.OUT)
spi = SPI(-1, baudrate=400000, polarity=1, phase=1, sck = Pin(14), mosi=Pin(13), miso=Pin(12))

# pincs.off()
# # # pincs.on()
init_ac()

xpre = 0
ypre = 0

xs = 1
ys = 1

position_x = 30
position_y = 10

while True:
    x, y, z = readReg()
    ##left 0- 120- -120 -0
    ##right 0 - 220

    xacc = x - xpre
    yacc = y - ypre

    if xs > 120:
        xs = x
        print('left')
        position_x -= 10
        if position_x < -70:
            position_x = 200
    elif xs < 0 and xacc > 100:
        xs = x + 255
    else:
        xs = x

    if x < -120:
        print('right')
        position_x += 10
        if position_x > 200:
            position_x = -70

    if ys >120:
        ys = y
        print('down')
        position_y += 5
        if position_y > 35:
            position_y = -10
    elif ys < 0 and yacc > 100:
        ys = y + 255
    else:
        ys = y

    if y< -120:
        print('up')
        position_y -= 5
        if position_y < -10:
            position_y = 35

    #print(x ,y ,z)

    xpre = x
    ypre = y

    oled.fill(0)
    oled.text('I LOVE IoT', position_x, position_y)
    oled.show()

    time.sleep_ms(200)