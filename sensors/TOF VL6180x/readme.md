## 2 I2C Devices mit selber Adresse

Die Sparkfun Tofs haben beide die HW Adresse 0x29 (29)  

Nach stundenlangem testen habe ich entschieden, dass es nicht möglich ist diese effizient anzusteuern.  

Deshlab wird ein I2C Multiplexer verwendet, der TCA9548A.
Die Inbetriebnahme anhand dieser Anleitung: 

    https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A

    Das dürfte das Problem effizient lösen