'''
Purpose - run a number of sequential internal resistance tests
		  in order to validate testing equipment and setup
Data generated by this file can be visualized by ContinuousPulseTestsPlot.py
'''

from src.equipments import lab_equipment as lb
import time
import os
import csv

#computer in the bay has 2x ni backends, no pyvisa-py

CURRENT_A_BASE = 0.2
CURRENT_A_PULSE = 2
BASE_TIME_MS = 1500
PULSE_TIME_MS = 2000
TIME_BETWEEN_PULSE_MS = 1000*60*15 #15 minutes

load = lb.BK8600()
load.toggle_eload(False)

dmm = lb.DMM_34410A()

def open_file():
	#generate new file name for logging in the current directory
	i = 0
	while os.path.exists("ContinuousPulse%s.csv" % i):
		i += 1
	filename = ("ContinuousPulse%s.csv" % i)
	
	file = open(filename, "wb")
	log = csv.writer(file)
	log.writerow(("Voltage", "Current"))
	return file, log

def logIV(csv_log):
	v = dmm.measure_voltage()
	i = load.measure_current()
	#log to file
	csv_log.writerow((v,i))
	print("{voltage}, {current}".format(voltage = v, current = i))

def pulse(csv_file, cb = CURRENT_A_BASE, bt = BASE_TIME_MS/1000, cp = CURRENT_A_PULSE, pt = PULSE_TIME_MS/1000):
	print("pulse")
	logIV(csv_file)
	#Set E-load output to base
	load.set_current(cb)
	#wait base time
	time.sleep(bt)
	logIV(csv_file)
	#set e-load output to pulse
	load.set_current(cp)
	#wait pulse time
	time.sleep(pt)
	logIV(csv_file)
	#set e-load output to 0A
	load.set_current(0)


def pulses(num, csv_file):
	#log("Time Between Pulses:{timetest}".format(timetest = TIME_BETWEEN_PULSE_MS))
	#log("Base Pulse:{bpulse}".format(bpulse = CURRENT_A_BASE))
	#log("Pulse Current:{cpulse}".format(cpulse = CURRENT_A_PULSE))
	for x in range(0,num):
		#log("{Pulse_Num}\n".format(Pulse_Num = x))
		pulse(csv_file)
		time.sleep(TIME_BETWEEN_PULSE_MS/1000)


def pulse_amp_var(csv_file):
	minI = input("Enter Minimum Current (int): ")
	maxI = input("Enter Maximum Current (int): ")
	step = input("Enter Step Size (int > 0): ")
	waitTime = input("Enter Time Between Pulses (s): ")

	for current in range(minI, maxI+1, step):
		pulse(csv_file, cp = current)
		time.sleep(waitTime)

def single_pulse_voltage_log():
	load.set_current(0)
	time.sleep(1)
	current = load.measure_current()
	start_time = time.time()
	while(time.time() - start_time < 5):
		voltage = dmm.measure_voltage()
		current = load.measure_current()
		time.sleep(1/1000) #1ms
		log.writerow((voltage, current))
	load.set_current(CURRENT_A_BASE)
	start_time = time.time()
	while(time.time() - start_time < 1.5):
		voltage = dmm.measure_voltage()
		current = load.measure_current()
		time.sleep(1/1000) #1ms
		log.writerow((voltage, current))
	load.set_current(CURRENT_A_PULSE)
	start_time = time.time()
	while(time.time() - start_time < 1.5):
		voltage = dmm.measure_voltage()
		current = load.measure_current()
		time.sleep(1/1000) #1ms
		log.writerow((voltage, current))
	load.set_current(0)
	start_time = time.time()
	while(time.time() - start_time < 120):
		voltage = dmm.measure_voltage()
		current = load.measure_current()
		time.sleep(1/1000) #1ms
		log.writerow((voltage, current))

def close_file(logfile):
	load.toggle_eload(False)
	logfile.close()
	print('\a') #Beep to notify test is finished
	
def test_pulses(number):
	logfile = open_file()
	pulses(number)
	close(logfile)


#run a script to do X number of pulses, then close the file and exit
if __name__ == "__main__":
	print("Continuous Pulse Testing for DC Internal Resistance")
	print("Test 1 = same pulse")
	print("Test 2 = increasing pulses")

	testNum = input("Which Test?")
	file, log = open_file()

	if(testNum == 1):
		num_pulses = input("Enter number of pulses to complete: ")
		pulses(num_pulses, log)
	elif(testNum == 2):
		pulse_amp_var(log)

	close_file(file)
	