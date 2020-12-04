import pyvisa
import time
from src.equipments.lab_equipment import Bk8600




#initialize instrument
inst = Bk8600()


# To Set E-Load in Amps
Current = input("Enter E-Load Current")
inst.set_current(Current)
Operation = "OFF"
#initialize instrument
while(Operation == "OFF"):
    Operation = input("Enter ON to turn on Output")
    if Operation == "ON":
        inst._set_input_on()
        print("Input On")
    time.sleep(0.002)


while Operation != "End":
    Operation = input("Enter:\n"+"M to meausre voltage and current\n"+"OFF to turn output off\n"+"End to close testing") 
    if Operation == "M":
        try:
            while True:
                print("current is: %d", inst.measure_current())
                print("voltage is: %d", inst.measure_voltage())
                time.sleep(0.002)
        except KeyboardInterrupt:
            pass

    elif Operation == 'OFF':
        inst._set_input_off() 
        print("Output OFF")
        time.sleep(0.002)
        while(Operation != "ON"):
            Operation = input("Enter ON to turn on Output")
            if Operation == "ON":
                Current = input("Enter E-Load Current")
                inst.set_current(Current)
                inst._set_input_on()
                print("Output On")
                time.sleep(0.002)
    
    elif Operation == 'End':
        inst._set_input_off() 
        time.sleep(1)
        print("Manual Testing Done")
    
    else :
        print("Error")
        time.sleep(0.002)


