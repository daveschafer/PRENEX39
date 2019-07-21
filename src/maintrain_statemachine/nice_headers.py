"""[Nice Headers]

Etwas für die Optik, muss auch sein.
"""

from termcolor import colored


def print_nice_headers(passed=False,cpu="NA", ram="NA", TOF1=False,TOF2=False, Sonic=False, Camera=False, MC01=False):

    #parse
    if (passed):
        passed_msg = "passed                     **"
    else:
        passed_msg = "failed                     **"
    
    if (TOF1):
        TOF1_msg = "Ready                      **"
    else:
        TOF1_msg = "Not Ready                  **"

    if (TOF2):
            TOF2_msg = "Ready                      **"
    else:
            TOF2_msg = "Not Ready                  **"

    if (Sonic):
            Sonic_msg = "Ready                      **"
    else:
            Sonic_msg = "Not Ready                  **"

    if (Camera):
            Camera_msg = "Ready                      **"
    else:
            Camera_msg = "Not Ready                  **"

    if (MC01):
            MC01_msg = "Ready                      **"
    else:
            MC01_msg = "Not Ready                  **"
        
    
    print(colored("************************************************", "green"))
    print(colored("************************************************", "red"))
    print("**          PRENEX39 - ControlPi              **")
    print("**--------------------------------------------**")
    print("**  Healthcheck:  ", passed_msg)
    print("**  CPU-Usage:    ",cpu ,"%                      **")
    print("**  free RAM:     ",ram," MB                  **")
    print("**  TOF1:         ",TOF1_msg)
    print("**  TOF2:         ",TOF2_msg)
    print("**  Sonic:        ",Sonic_msg)
    print("**  Camera:       ",Camera_msg)
    print("**  MC-Com:       ",MC01_msg)
    print("**--------------------------------------------**")
    print(colored("************************************************", "red"))
    print(colored("************************************************", "green"))
    print("============================================================================")
