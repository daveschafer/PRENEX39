import camera
import config
from config import parse_config
from camera import Camera
import debug_detector


def main():
    """
    Main entry point
    """
    print("[INFO] entry main()")
    configfile = "configs/molly.ini"
    print("[INFO] start with config file: %s" % configfile)
    config = parse_config(configfile)

    process_pool_size = config["detector"].getint("pool_size")
    camera = Camera.from_config(config["camera"])

    debug_detector.start_detection(camera, process_pool_size)


if __name__ == "__main__":
    main()
