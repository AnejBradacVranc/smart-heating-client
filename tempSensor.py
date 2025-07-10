import os
import glob
import time


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
	
def read_temp_raw():
	f=open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
	
def read_temp():
	lines = read_temp_raw()
	#Until sensor is ready wait and read lines until you reach line with YES
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	#When you find line with t=, process it
	equals_pos = lines[1].find('t=')	
	if equals_pos != -1:
		#Take everything after t=
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c

