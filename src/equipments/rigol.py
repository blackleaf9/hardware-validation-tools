import pyvisa
import time
import datetime
#from ds1054z import DS1054Z

#scope = DS1054Z('USB0::6833::1230::DS1ZA182511136::0::INSTR')
#print("Connected to: ", scope.idn)
# all voltages are measured in Volts and Time is measured in seconds
class DS1054Z(object):
    # Initialize to the bay's DS1054Z address through USB
	def __init__(self, resource_id='USB0::6833::1230::DS1ZA182511136::0::INSTR'):
		rm = pyvisa.ResourceManager()
		self.inst = rm.open_resource(resource_id)
		print("Connected to %s\n" % self.inst.query("*IDN?"))
		time.sleep(0.001)
		self.inst.write("*RST")
	
	def screencapture(self, filename='', auto_view=True):
		buf = self.inst.query_binary_values(':DISP:DATA? ON,0,PNG', datatype='B')
		if (filename == ''):
			filename = "rigol_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".png"
		with open(filename, 'wb') as f:
			print('Capturing screen to'+ filename)
			f.write(bytearray(buf))
			f.close()
		if auto_view:
			open(filename)

	def autoscale(self):
		self.inst.write(':AUT')

	def single_trigger(self):
		self.inst.write(':SING')
		
	def force_trigger(self):
		self.inst.write(':TFOR')
		
	def run_trigger(self):
		self.inst.write(':RUN')


	def setup_channel(self, channel=1, on=1, offset=0.0, volts_per_div=1.0, probe=1.0,time_per_div=0.001,delay=0.001):
		#unit for Voltage is Volts, unit for time is seconds
		if (on == 1):
			self.inst.write(':CHAN' + str(channel) + ':DISP ' + 'ON')
			self.inst.write(':CHAN' + str(channel) + ':SCAL ' + str(volts_per_div))
			self.inst.write(':CHAN' + str(channel) + ':OFFS ' + str(offset*volts_per_div))
			self.inst.write(':CHAN' + str(channel) + ':PROB ' + str(probe))
			self.inst.oscilloscope.write(':TIM:MAIN:SCAL ' + str(time_per_div))
			self.inst.write(':TIM:MAIN:OFFS ' + str(delay))
			print ("Turned on CH" + str(channel) + ", position is " + str(offset) + " divisions from center, " + str(volts_per_div) + " volts/div, scope is " + str(probe) + "x")
			print ("Timebase was set to " + time_per_div + " per division")
		else:
			self.inst.write(':CHAN' + str(channel) + ':DISP OFF')
			print ("Turned off channel " + str(channel))

	def reset(self):
		self.inst.write("*RST")
		print("Oscilloscope Reset")	

	def end_session(self):
		self.inst.close()
		print("Ended USB session with oscilloscope")
	
	def measure_rmsvoltage(self, channel=1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'VRMS' + ',CHAN' + str(channel)))

	def measure_maxvoltage(self, channel=1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'VMAX' + ',CHAN' + str(channel)))

	def measure_minvoltage(self, channel=1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'VMIN' + ',CHAN' + str(channel)))

	def peak_to_peak_voltage(self,channel =1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'VPP' + ',CHAN' + str(channel)))

	def average_voltage(self,channel=1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'VAVG' + ',CHAN' + str(channel)))

	def frequency(self,channel = 1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'FREQ' + ',CHAN' + str(channel)))

	def period(self,channel=1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'PER' + ',CHAN' + str(channel)))

	def top_voltage(self, channel = 1):
		#voltage between top of waveform and gnd
		return float(self.inst.query(':MEAS:ITEM? ' + 'VTOP' + ',CHAN' + str(channel)))
	
	def bottom_voltage(self,channel = 1):
		#voltage between bottom of waveform and ground
		return float(self.inst.query(':MEAS:ITEM? ' + 'VBAS' + ',CHAN' + str(channel)))
	
	def top_to_base_voltage(self, channel=1):
		#voltage between top of waveform and base of waveform
		return float(self.inst.query(':MEAS:ITEM? ' + 'VAMP' + ',CHAN' + str(channel)))

	def upper_voltage(self,channel=1):
		#Threshold maximum voltage value
		return float(self.inst.query(':MEAS:ITEM? ' + 'VUP' + ',CHAN' + str(channel)))

	def lower_volatge(self,channel=1):
		# Threshols minimum voltage value
		return float(self.inst.query(':MEAS:ITEM? ' + 'VLOW' + ',CHAN' + str(channel)))

	def overshoot_voltage(self,channel=1):
		#percentage difference of top of waveform from max threshold
		return float(self.inst.query(':MEAS:ITEM? ' + 'OVER' + ',CHAN' + str(channel)))

	def pershoot_voltage(self,channel=1):
		#percentage difference of bottom of waveform from min threshold
		return float(self.inst.query(':MEAS:ITEM? ' + 'PRES' + ',CHAN' + str(channel)))
	
	def rise_time(self, channel= 1):
		#time for signal to rise from lower voltage threshold to higher voltage threshold
		return float(self.inst.query(':MEAS:ITEM? ' + 'RTIM' + ',CHAN' + str(channel)))

	def fall_time(self, channel=1):
		#time for signal to fall from higer voltage threshold to lower voltage threshold
		return float(self.inst.query(':MEAS:ITEM? ' + 'FTIM' + ',CHAN' + str(channel)))

	def max_voltage_time(self,channel=1):
		#time of max voltage
		return float(self.inst.query(':MEAS:ITEM? ' + 'TVMAX' + ',CHAN' + str(channel)))
	
	def min_voltage_time(self,channel=1):
		#time of min voltage
		return float(self.inst.query(':MEAS:ITEM? ' + 'TMIN' + ',CHAN' + str(channel)))

	def rising_delay_time(self,channel = 1):
		#time difference between the falling edges of source 1 and source 2. Negative delay indicates that the selected falling edge of source 1 occurred after that of source 2
		return float(self.inst.query(':MEAS:ITEM? ' + 'RDEL' + ',CHAN' + str(channel)))

	def falling_delay_time(self,channel = 1):
		#time difference between the falling edges of source 1 and source 2. Negative delay indicates that the selected falling edge of source 1 occurred after that of source 2
		return float(self.inst.query(':MEAS:ITEM? ' + 'FDEL' + ',CHAN' + str(channel)))

	def positive_slew_rate(self, channel = 1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'PSLEW' + ',CHAN' + str(channel)))

	def negative_slew_rate(self,channel = 1):
		return float(self.inst.query(':MEAS:ITEM? ' + 'NSLEW' + ',CHAN' + str(channel)))
	