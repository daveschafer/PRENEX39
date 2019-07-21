import signalerkennung.camera
from signalerkennung.camera import Camera
import signalerkennung.config
from signalerkennung.config import parse_config
import signalerkennung.number_detector



## Für Test/Debug Zwecke geeignet
def main(signalmode="info"):
    """
    Main entry point
    """
    print("[INFO] entry main()")
    configfile = "configs/prenex.ini"
    print("[INFO] start with config file: %s" % configfile)
    config = parse_config(configfile)

    camera = Camera.from_config(config["camera"])

    if(signalmode=="info"):
        print("[INFO] Infosignal Detect starten")
        number_detector.signal_detection(camera,signalmode="info")
    elif(signalmode=="halt"):
        print("[INFO] Haltesignal Detect starten")
        number_detector.signal_detection(camera,signalmode="halt")
    elif(signalmode=="start"):
        print("[INFO] Startsignal Detect starten")
        number_detector.start_startsignal_detection(camera)
    #remove camera after match
    del camera


def debug_withcam(camera, signalmode="info", infosig_nr=0):
    camera = camera
    
    if(signalmode=="info"):
        print("[INFO] Infosignal Detect starten")
        number_detector.signal_detection(camera,signalmode="info")
    elif(signalmode=="halt"):
        print("[INFO] Haltesignal Detect starten")
        number_detector.signal_detection(camera,signalmode="halt",infosig_nr=infosig_nr)
    elif(signalmode=="start"):
        print("[INFO] Startsignal Detect starten")
        number_detector.start_startsignal_detection(camera)
    
    print("debug done")


def init_camera():
    print("[INFO] Camera Initiator")
    #configfile = "configs/prenex.ini"
    configfile = "/home/pi/PREN/maintrain_statemachine/signalerkennung/configs/prenex.ini"

    print("[INFO] start with config file: %s" % configfile)
    config = parse_config(configfile)
    camera = Camera.from_config(config["camera"])

    return camera

if __name__ == "__main__":
    main()
