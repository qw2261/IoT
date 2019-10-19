# IoT

## Lab配置：

1. [跟随lab配好相关设置](http://www.1zlab.com/wiki/micropython-esp32/)
2. 在mac上安装picocom
3. 打开接口端口为：
   1. 先source
   2. mpfshell
   3. open tty.SLAB_USBtoUART
   4. 打开新终端：sudo picocom -b 115200 /dev/tty.SLAB_USBtoUART
4. repl中
   1. `CTRL + C` 中断程序
   2. `CTRL + D` 软重启
   3. `CTRL + E` 进入代码片段粘贴模式
   4. ```CTRL + Q```退出



## Lab 3. **Bus Communication: I2C and SPI**

## Hardware SPI bus

The hardware SPI is faster (up to 80Mhz), but only works on following pins: `MISO` is GPIO12, `MOSI` is GPIO13, and `SCK` is GPIO14. It has the same methods as the bitbanging SPI class above, except for the pin parameters for the constructor and init (as those are fixed).



## Lab 5. **Embedded Servers**

[**android-google-cloud-speech-api**](https://github.com/Cloudoki/android-google-cloud-speech-api)

[**Google-Cloud-Speech-API**](https://github.com/sujitpanda/Google-Cloud-Speech-API)

[**android-google-cloud-speech-api**](https://github.com/Cloudoki/android-google-cloud-speech-api)



ngrok:

启动端口： python3 -m http.server --cgi 8000

启动http的端口： ./ngrok http 8000