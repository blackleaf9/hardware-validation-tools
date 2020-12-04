import pyvisa
import time
from src.equipments.rigol import DS1054Z

Operation = "OFF"
while(Operation == "OFF"):
    Operation = input("Enter ON to turn on Output")
    if Operation == "ON":
        inst = DS1054Z()
        print("DS1054Z ON")
    time.sleep(0.002)
#initialize instrument


print("Setting up Inst")
inst.setup_channel()
inst.autoscale()
while Operation != "End":
    Operation = input("Enter:\n"+"SC for screen capture\n"+"V to meausre rms voltage\n" + "f to measure frequency\n"+"P to measure period\n"+" End to close testing") 
    if Operation == "SC":
        inst.screencapture()
    elif Operation == "V":
        print("rms voltage is: %d", inst.measure_rmsvoltage())

    elif Operation == 'f':

        print("frequency is: %d", inst.frequency())

    elif Operation == 'p':
        print("Period is: %d", inst.period())

    elif Operation == 'End':
        print("Manual Testing Done")
    else :
        print("Error")
        time.sleep(0.001)



