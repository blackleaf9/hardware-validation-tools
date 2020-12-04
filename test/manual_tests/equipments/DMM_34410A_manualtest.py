import pyvisa
import time
from src.equipments.lab_equipment import DMM_34410A




#initialize instrument
inst = DMM_34410A()
Operation = "ON"
while Operation != "End":
    Operation = input("Enter:\n"+"V to meausre voltage\n" + "C to measure current\n"+" End to close testing") 
    if Operation == "V":
        try:
            while True:
                print("voltage is: %d", inst.measure_voltage())
                time.sleep(0.001)
        except KeyboardInterrupt:
            pass

    elif Operation == 'C':
        try:
            while True:
                print("current is: %d", inst.measure_current())
                time.sleep(0.001)
        except KeyboardInterrupt:
            pass
    elif Operation == 'End':
        print("Manual Testing Done")
    else :
        print("Error")
        time.sleep(0.001)






