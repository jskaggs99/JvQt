# movement.py

import serial2marlin as s2m
import numpy as np

#perovskite = solarcelltray(vmin)

class solarcelltray():
"""
x0: bottom left corner of the bottom left cell
y0: bottom left corner of the bottom left cell


"""
# Establishing a dictionary under the solarcelltray to keep track of physical and scan parameters. 

	tray_dict = {'Profile': None,
					'vmin':vmin, 'vmax':vmax}

	def __init__(self, profile, vmin, vmax, vnum, rate, chemistry):
		self.profile = 'full30tray'
		# Set up scan params
		self.vmin = vmin
		self.vmax = vmax
		self.vnum = vnum
		self.rate = rate
		self.chemistry = chemistry
		self.Voltage = None
		self.CurrentDensity = None

		# Physical tray triggers
		self.homed = False

		# Physical tray parameters and profiles
		if self.profile == 'full30tray':
			self.x0 = 10 #x position of corner cell, mm
			self.y0 = 10 #y position of corner cell, mm
			self.xoffset = 30 #x spacing between cells, mm
			self.yoffset = 30 #y spacing between cells, mm
			self.xnum = 5
			self.ynum = 5
			self.pixels = 3

		elif self.profile == 'halftrays'
			self.x0 = 10
			self.y0 = 10
			self.xoffset = 30
			self.yoffset = 30 
			self.xnum = 5
			self.ynum = 5
			self.pixels = 3

		else
			print('Need to select a tray profile or initialize one in the code (movement.py)')
			# Can i get this to send to the output window of the gui?

	def automated_JV(self):
		# Define the profile here. default is scan cells 1 through 25/30. 
		if self.profile == 
		x = 0

	def measure_JV(vmin, vmax, pts, rate):
		# Set up the jv sweep variables
	 	vmeas = np.linspace(vmin, vmax, pts)
	 	jmeas = [[]] # currentdensity array
	 	pixel_index = np.arange(1, pixels + 1) # np.arange(1,7) -> [1,2,3,4,5,6]

	 	# Lower the z-contact probe
	 	s2m.zprobe.lower_zstamp() # fake function, part of the zstamp class?

	 	# Open the shutter
	 	shutter_cnt.Shutter.shutter_open()

	 	# Proceed with measurements of each pixel
	 	for p_ in pixel_index:
	 		pixelswitch_cnt.Pixelswitch.turn_on_pixel(pixelval=p_)  # turn on pixel p_
	  		self.CurrentDensity[p_] = take_measurement(vmeas, jmeas) # store the measurement into the dictionary
	  		self.Voltage[p_] = vmeas
	    # return vmeas, jmeas

	  # light_off() # fake function
	  	shutter_cnt.Shutter.shutter_close()
		pixelswitch_cnt.Pixelswitch.turn_off_all()
		keithley_cnt.Keithley.inst_output_off()

	def measure_tray(x0, y0, xoffset, yoffset, xnum, ynum):
		xp = [x0 + xoffset*i for i in range(xnum)]
		yp = [y0 + yoffset*i for i in range(ynum)]
	 	for x in xp:
			for y in yp:
				move_to(x,y)
	    		measure_JV(...)

	 def take_measurement(vmeas, jmeas):
	 	# vmeas/voltage_arr/voltage array is a numpy array of the specific voltages that the solar cell will be biased at. 
	 	for v in vmeas:
	    		jmeas.append(keithley_cnt.Keithley.inst_set_source_volt_value(voltage=v_))
	    return jmeas