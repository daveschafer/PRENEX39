###################################
## PRENEX39 RPI Installer Script ##
##                               ##
##  use Base Image Stretch Lite  ##
##                               ##
###################################

# Check if sudo is used
if [ "$(id -u)" != 0 ]; then
  echo 'Sorry, you need to run this script with sudo'
  exit 1
fi

#Colors
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
cyan=`tput setaf 6`
reset=`tput sgr0`
#echo "${red}red text ${green}green text${reset}"

##
# Base OS Update
##

echo "[1] : Updating Base System OS"
apt-get update && apt-get upgrade -y
#fixing broken deps, just in case
#apt --fix-broken install -y
echo "[1] : Completed"
echo "${yellow}========================================================${reset}"


###
#
# Defining Packages 2 be installed
#
###

PACKAGES="cmake curl e2fslibs build-essential cifs-utils g++ gcc gcc-4.6-base gcc-4.7-base gcc-4.8-base gcc-4.9-base gcc-5-base gcc-6-base git htop i2c-tools initramfs-tools kmod libapt-inst2.0 libapt-pkg5.0 libc-bin libc6 libdbus-1-3 libgnutls30 python3 python3-pip python3-rpi.gpio python3-smbus wiringpi python3-picamera python-pip espeak python3-scipy python3-h5py"

echo "[2] : Installing Linux Packages"
echo "[2] : Package List: "
echo "$PACKAGES"

echo "${cyan}========================================================${reset}"

#Python 3.7 - Optional
#echo "[2.1] : Installing Python 3.7 (optional, not needed)"
#sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
#wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
#tar xf Python-3.7.2.tar.xz
#cd Python-3.7.2
#./configure
#make -j 4
#make altinstall
#cd ..
#rm -r Python-3.7.2
#rm Python-3.7.2.tar.xz
#echo "[2.1] : Python3.7 installed, call with (python3.7 yourscript.py)"

apt-get install $PACKAGES -y

echo "[2] : Completed"
echo "${yellow}========================================================${reset}"

###
#
# Defining Python-PIP Packs 2 be installed
#
###

PIPPACKAGES="Adafruit-Blinka adafruit-circuitpython-busdevice adafruit-circuitpython-vl6180x Adafruit-GPIO adafruit-io Adafruit-PlatformDetect Adafruit-PureIO board rpi-ws281x RPi.GPIO smbus2 urllib3 Werkzeug pyserial numpy termcolor h5py" #no picam and no pillow (v6 broken)

echo "[3] : upgrading pip3 setuptools"
pip3 install --upgrade setuptools

echo "[3] : Installing Python Packs (pip)"
echo "[3] : PIP List: "
echo "$PIPPACKAGES"

pip3 install $PIPPACKAGES

echo "${yellow}========================================================${reset}"

echo "[3] : Enlarge SWAP to 2Gibi"

#Enlarging the Swap File, else Pi will explode
sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start

echo "${yellow}========================================================${reset}"


echo "[3] : Installing Tensorflow (~20min)"

pip3 install tensorflow

echo "[3] : Installing KERAS (~90min)"

pip3 install keras

echo "${yellow}========================================================${reset}"


echo "[3] : Installing Pillow 5.4.1 (pip) because v6 has broken dependencies"

pip3 install Pillow==5.4.1

#installing pip (python2) voice library
echo "[3] : installing pip (python2) voice library"

pip install pyttsx3

echo "[3] : Completed"
echo "${yellow}========================================================${reset}"
echo "...going to sleep for 30s, please check the Log above"
sleep 30s
echo "${yellow}========================================================${reset}"



###
#
# Defining Special Packages 2 be installed (opencv, Tesseract...)
#
###

echo "[4] : Installing Special Packages"
echo "[4] : Special Packages List: "

echo "[4.1] : Opencv 4.1"

echo "[4.1.1] : Install Opencv 4.1 from Git"

#Commands for Opencv 3.4.4
#prerequisits & Dependencies
#apt install libatlas3-base libsz2 libharfbuzz0b libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4 -y
# main opencv 3.4
#pip3 install opencv-contrib-python

#CV4: Build Tools
apt-get install build-essential cmake unzip pkg-config -y

#Libraries Image and Video
apt-get install libjpeg-dev libpng-dev libtiff-dev -y
apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
apt-get install libxvidcore-dev libx264-dev -y

#numerical optimization packages
apt-get install libatlas-base-dev gfortran python3-dev -y

#Download and Install OpenCV

wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.0.zip

unzip opencv.zip
unzip opencv_contrib.zip

mv opencv-4.1.0 opencv
mv opencv_contrib-4.1.0 opencv_contrib

cd opencv
mkdir build
cd build

#just in case
apt-get install cmake -y

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=/home/pi/install/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..



echo "${yellow}==========================Start CV Compilation==============================${reset}"
make -j4
echo "${yellow}==========================Completed CV Compilation==============================${reset}"

make install
ldconfig

cd ..
cd ..
#cleanup opencv install
rm -r opencv
rm -r opencv_contrib

rm opencv.zip
rm opencv_contrib.zip

echo "${yellow}========================================================${reset}"

echo "[4.2] : Tesseract 4"
echo "[4.2.1] : install tesseract 4 from git"

#For Tesseract 3.04 version:
#apt-get install tesseract-ocr -y

#Prerequisits
apt-get install automake g++ git libtool libleptonica-dev make pkg-config -y
apt-get install --no-install-recommends asciidoc -y

git clone --depth 1  https://github.com/tesseract-ocr/tesseract.git 
cd tesseract/
./autogen.sh
./configure

echo "${yellow}==========================Start Tesseract Compilation==============================${reset}"
make -j4
echo "${yellow}==========================Completed Tesseract Compilation==============================${reset}"

make install
ldconfig
tesseract -v
cd ..

#cleanup
rm -r tesseract

echo "${yellow}========================================================${reset}"

echo "[4] : Shrinking SWAP to 256"

#Shrinking the Swap File again, else SD Card will implode
sed -i 's/CONF_SWAPSIZE=2048/CONF_SWAPSIZE=256/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start

echo "${yellow}========================================================${reset}"

#Add digits traineddata, todo

# https://github.com/Shreeshrii/tessdata_shreetest
# https://github.com/tesseract-ocr/tesseract/wiki/FAQ#where-are-the-language-models-traineddata-files-for-tesseract-installed

echo "[4.2.2] : install python tesseract wrapper"
pip3 install pytesseract

echo "[4] : Completed"
echo "${yellow}========================================================${reset}"

##
# Tweaking Operating System
##

#Replace the Existing config.txt file with our version so we have:
# gpu mem reduced | Camera activated | i2c | uart

echo "[5] : Tweaking OS"
mv /boot/config.txt /boot/config_default.txt
cp -f config.txt /boot/config.txt

echo "[5] : Setup I2C"

sh ./setup_i2c.sh

echo "[5] : Installing Adafruit Libraries for I2C"
pip3 install RPI.GPIO
pip3 install adafruit-blinka
#multiplexer library
pip3 install adafruit-circuitpython-tca9548a

echo "[5] : Completed"

echo "${yellow}========================================================${reset}"

echo "[6] : Cleanup Installations"

#cleanup python stuff
#apt-get --purge remove build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
apt-get autoremove -y
apt-get clean

#multiplexer library again
pip3 install adafruit-circuitpython-tca9548a
#vl6180x again
pip3 install adafruit-circuitpython-vl6180x
#pyserial again
pip3 install pyserial

echo "[6] : Completed"

echo "${yellow}========================================================${reset}"

echo "${green}[Complete] : Installation is completed!${reset}"
echo "${cyan}[Info] : You need to activate I2C with Raspi-Conf${reset}"
echo "${cyan}[Info] : You may need to activate UART (Serial) with Raspi-Conf${reset}"
echo "${cyan}[Info] : OpenCV 4 & Tesseract 4 - ready 2 read some numbers${reset}"
echo "${cyan}[Info] : You may need to install tca lib again 'pip3 install adafruit-circuitpython-tca9548a'${reset}"
echo "${cyan}[Info] : Please reboot Pi (sudo reboot now)${reset}"


echo "${yellow}========================================================${reset}"