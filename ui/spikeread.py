#!/usr/bin/python3
import serial, sys
import threading

serialdata = ""



def serialReader():
    while True:
        try:
            ser = serial.Serial("/dev/ttyACM0")  # open serial port
            print(ser.name)         # check which port was really used
            line = ""
            while not ("PROGEXITPROG" in line):
                raw = ser.readline()
                line = raw.decode().strip().split("TXTSPTXT")
                serialdata = line[1]
                try:
                    print(line[1])
                except Exception as exc:
                    print(exc)
                    pass
                # time.sleep(0.1)
            ser.close()
        except:
            ser.close()
            print("done")


def getSpikeData():
    return serialdata

def init():
    x = threading.Thread(target=serialReader)
    x.start()


