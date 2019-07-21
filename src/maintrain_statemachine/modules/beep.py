from time import sleep
import os
import _thread


def beep(times=1):
    _thread.start_new_thread(__beep_async, (times,))
    print("beep done '%s' times" %times)

def __beep_async(times=1):
    for x in range(times):
        #os.system("omxplayer -o local beep.mp3")
        os.system("omxplayer -o local /home/pi/PREN/maintrain_statemachine/modules/beep.mp3 > /dev/null")
