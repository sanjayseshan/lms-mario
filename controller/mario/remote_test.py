#!/usr/bin/python3

# Echo client program
import socket,time
import ev3dev.ev3 as ev3
from time import sleep


ult1 = ev3.InfraredSensor(address='ev3-ports:in1')
ult2 = ev3.InfraredSensor(address='ev3-ports:in2')
ult3 = ev3.InfraredSensor(address='ev3-ports:in3')
ult4 = ev3.InfraredSensor(address='ev3-ports:in4')

ult1.mode = 'IR-PROX'
ult2.mode = 'IR-PROX'
ult3.mode = 'IR-PROX'
ult4.mode = 'IR-PROX'

while True:
    print("sens1:" + str(ult1.value()))
    print("sens2:" + str(ult2.value()))
    print("sens3:" + str(ult3.value()))
    print("sens4:" + str(ult4.value())+"\n")
