#!/usr/bin/env python3

from telnetlib import Telnet
import sys
import re

avrip="10.1.210.194"
volStepSize = 2

connection = Telnet(avrip)


try:
   avr_function = sys.argv[1]
except IndexError:
    print("No argument provided")
    sys.exit(100)

if (avr_function == "MUTE"):
    connection.write(b"MU?")
    mutestate = connection.read_until(b"\r",timeout=1).decode("utf-8").rstrip()
    if (mutestate == "MUOFF"):
        connection.write(b"MUON")
    if (mutestate == "MUON"):
        connection.write(b"MUOFF")
elif ((avr_function == "VOLUP") | (avr_function == "VOLDOWN")):
    connection.write(b'MV?')
    currentVolInfo = connection.read_until(b"MVMAX",timeout=1).decode("utf-8").rstrip()
    volREobj = re.compile('^MV(\d*)')
    volMatchGroup = volREobj.match(currentVolInfo)
    currnetVol = int(volMatchGroup.group(1))
    newvol = 0
    if (avr_function == "VOLUP"):
        if (currnetVol < 100):
            newVol = currnetVol + volStepSize
        elif (currnetVol > 100):
            newVol = currnetVol + (volStepSize * 10)
    elif (avr_function == "VOLDOWN"):
        if (currnetVol < 100):
            newVol = currnetVol - volStepSize
        elif (currnetVol > 100):
            newVol = currnetVol - (volStepSize * 10)
    newVolCommand = "MV" + str(newVol)
    connection.write(newVolCommand.encode(encoding='UTF-8'))
elif (avr_function == "PWR"):
    connection.write(b'PW?')
    currnetPwrStatus = connection.read_until(b"\r",timeout=1).decode("utf-8").rstrip()
    if (currnetPwrStatus == "PWON"):
        connection.write(b'PWSTANDBY')
    if (currnetPwrStatus == "PWSTANDBY"):
        connection.write(b'PWON')
elif (avr_function == "INPUT"):
    connection.write(b'SI?')
    currnetInput = connection.read_until(b"\r",timeout=1).decode("utf-8").rstrip()
    if (currnetInput != 'SIPHONO'):
        connection.write(b'SIPHONO')
    if (currnetInput == 'SIPHONO'):
        connection.write(b'SIMPLAY')
else:
    print("No valid argument provided")

connection.close()
