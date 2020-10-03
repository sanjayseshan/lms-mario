from util.print_override import spikeprint;print = spikeprint
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer

hub = PrimeHub() 

from util.print_override import spikeprint;print = spikeprint
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer

hub = PrimeHub()
color = ColorSensor('D')
del print # removes print to console functionality; restores standard implementation
x=0
def printSP(input): #use to filter pi serial
    print("TXTSPTXT"+str(input)+"TXTSPTXT")

while True:
    # Check for win condition
    if (color.get_color() == 'red'):
        # tell pi that mario has won"
        printSP("9;red:(1,2)")
        # cheer to show Mario wins
        hub.light_matrix.write('M')
    else:
        printSP("0;none:(1,2)")
        hub.light_matrix.off()
