## Wie via SCP von Windows Powershell hochladen?

Basics:

	scp "pfad zum file" username@pi-Ip-Adresse:"pfad/auf/dem/pi"

Example:

	scp .\KY-032_RPi_HindernisDetektor.py pi@192.168.0.119:/home/pi/sensor/