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

## Lecture 3. INTERFACING WITH THE PHYSICAL WORLD



## Lab 3. **Bus Communication: I2C and SPI**

## Hardware SPI bus

The hardware SPI is faster (up to 80Mhz), but only works on following pins: `MISO` is GPIO12, `MOSI` is GPIO13, and `SCK` is GPIO14. It has the same methods as the bitbanging SPI class above, except for the pin parameters for the constructor and init (as those are fixed).









## Lab 4. **Bus Communication: I2C and SPI**

https://focusonforce.com/integration-and-data-loading/rest-api-using-weather-example/





https://hackaday.io/project/25359-esp8266-twitter-client/log/61061-using-twitter-apis-with-esp8266



https://hackaday.io/project/25359-esp8266-twitter-client



https://docs.singtown.com/micropython/zh/latest/esp32/esp32/tutorial/network_tcp.html



https://developer.atlassian.com/server/crowd/json-requests-and-responses/





http://www.json.org/JSONRequest.html