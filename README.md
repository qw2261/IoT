# IoT
The courseworks and codes of my own projects for the course IoT in Columbia.



## Lab Configuration：

1. Follow the [Basics](http://www.1zlab.com/wiki/micropython-esp32/) steps.
2. Install picocom in Mac.
3. The step to open the shell of board：
   1. Initially source your python environment to the one you have installed mpfshell.
   2. Then in a appropriate path enter **mpfshell**.
   3. Then in the shell, enter **open tty.SLAB_USBtoUART**
   4. Open another terminal to enter **sudo picocom -b 115200 /dev/tty.SLAB_USBtoUART**.
4. In the **repl**
   1. `CTRL + C` to interrupt the program;
   2. `CTRL + E` to enter the mode that you can paste your code;
   3. `CTRL + D` to run your code;
   4. ```CTRL + Q``` to exit repl.









## Lab 3. **Bus Communication: I2C and SPI**

### Hardware SPI bus

The hardware SPI is faster (up to 80Mhz), but only works on following pins: `MISO` is GPIO12, `MOSI` is GPIO13, and `SCK` is GPIO14. It has the same methods as the bitbanging SPI class above, except for the pin parameters for the constructor and init (as those are fixed).



## Lab 5. **Embedded Servers**

[**android-google-cloud-speech-api**](https://github.com/Cloudoki/android-google-cloud-speech-api)

[**Google-Cloud-Speech-API**](https://github.com/sujitpanda/Google-Cloud-Speech-API)

[**android-google-cloud-speech-api**](https://github.com/Cloudoki/android-google-cloud-speech-api)



ngrok:

Start a server： python3 -m http.server --cgi 8000

Make the server to be accessible from outside internet： ./ngrok http 8000

