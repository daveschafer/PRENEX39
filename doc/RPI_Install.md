# Beschreibung RPI Installation 

1. Start mit Clean Image von Raspberry (Stretch Lite)

2. Auf dem Pi unter "/home/pi" einen Ordner "install" erstellen

3. Ganzen Inhalt dieses Ordners auf Pi "/home/pi/install" kopieren und 'sudo ./rpi_install.sh' starten

3.1. Um ein Log zu erhalten, start mit 'sudo ./rpi_install.sh | tee rpi_install.log'

4. Installation startet und installiert: Updates, Sensor Libraries, OpenCV4, Tesseract4

*Die OpenCV4 Compilation dauert ca 2h, alternativ kann via pip Opencv3.4 installiert werden, das ist precompiled*

5. Manuell noch die Custom Tesseract library für Numbers nachladen

https://github.com/Shreeshrii/tessdata_shreetest


# Install Packages Manually (list not complete!)


## Tesseract 4

### Prerequisits

Check if not already installed.

    sudo apt-get install g++ # or clang++ (presumably)
    sudo apt-get install autoconf automake libtool
    sudo apt-get install pkg-config
    sudo apt-get install libpng-dev
    sudo apt-get install libjpeg8-dev
    sudo apt-get install libtiff5-dev
    sudo apt-get install zlib1g-dev


## Tesseract 4 Main Installation

Follow these Instructions:

https://github.com/tesseract-ocr/tesseract/wiki/Compiling-%E2%80%93-GitInstallation

