# serial2marlin
"""
Will take care of sending G-code through serial to Marlin. 

"""
import serial
import time

class SerialConnect():
	
	def __init__(self, COM = 'COM5', baudrate = 115200):
		self.COM = COM
		self.baudrate = baudrate
		self.serial_handle = None

	def openserial(self, COM = 'COM5', baudrate = 115200):
		#Establishes a serial communication between the driverboard.
		ser = serial.Serial(COM, baudrate)
		ser.write(b'\n\n')
		time.sleep(1)
		self.serial_handle = ser
		return ser

	def closeserial(self):
		self.serial_handle.close()

	def send2marlin(self, text, COM = 'COM6', baudrate = 115200, *args, **kwargs):
		""" 
		Sends G-Code as an input into Marlin. Removes the need for pronterface.
		"""
		ser = self.serial_handle
		text = text + '\n'
		print(text)
		text = str.encode(text) # encodes it into bytes

		ser.write(b'\n\n') # wakes up the serial port
		time.sleep(1)
		ser.write(text)
		time.sleep(1)
		# ser.write(b'G28 X0\n') # My second issue comes up when I'm not sure of the line ending character that the M2 expects (maybe \n, \r or even \r\n)
		
	def manualgcodesender():
		#Probably useless
		x=1

	def flushbuffer(self):
		self.serial_handle.reset_input_buffer()

class xystage():
	connection_dict = {'xstepper': {'COM': 'ASRL3::INSTR', 'connection':None, 'movementhistory': None, 'homed': False},
                       'ystepper': {'COM': 'ASRL3::INSTR', 'connection':None, 'movementhistory': None, 'homed': False}
						}
	def move_to(self, x,y):
		#check to see if x and y are both given. 
		# s2m.send2marlin()
		s2m.send2marlin('G0 X'+ str(x))
		s2m.send2marlin('G0 Y'+ str(y))

	def homestage(self):
		s2m.send2marlin(G28)
		self.homed = true

class zprobe():
	connection_dict = {'zstepper': {'COM': 'ASRL3::INSTR', 'connection':None, 'movementhistory': None, 'homed': False}
						}
	def move_to(self, z):
		s2m.send2marlin('G0Z'+ str(z))

	def lift_down(self):
		send2marlin(G0Z5)
	
	def homestage(self):
		s2m.send2marlin(G28)
		self.homed = true


	# #!/usr/bin/python
	# """\
	# Simple g-code streaming script
	# https://github.com/bborncr/gcodesender.py/blob/master/gcodesender.py
	# """
	 
	# import serial
	# import time
	# import argparse

	# parser = argparse.ArgumentParser(description='This is a basic gcode sender. http://crcibernetica.com')
	# parser.add_argument('-p','--port',help='Input USB port',required=True)
	# parser.add_argument('-f','--file',help='Gcode file name',required=True)
	# args = parser.parse_args()
	 
	# ## show values ##
	# print ("USB Port: %s" % args.port )
	# print ("Gcode file: %s" % args.file )


	# def removeComment(string):
	# 	if (string.find(';')==-1):
	# 		return string
	# 	else:
	# 		return string[:string.index(';')]
	 
	# # Open serial port
	# #s = serial.Serial('/dev/ttyACM0',115200)
	# s = serial.Serial(args.port,115200)
	# print 'Opening Serial Port'
	 
	# # Open g-code file
	# #f = open('/media/UNTITLED/shoulder.g','r');
	# f = open(args.file,'r');
	# print 'Opening gcode file'
	 
	# # Wake up 
	# s.write("\r\n\r\n") # Hit enter a few times to wake the Printrbot
	# time.sleep(2)   # Wait for Printrbot to initialize
	# s.flushInput()  # Flush startup text in serial input
	# print 'Sending gcode'
	 
	# # Stream g-code
	# for line in f:
	# 	l = removeComment(line)
	# 	l = l.strip() # Strip all EOL characters for streaming
	# 	if  (l.isspace()==False and len(l)>0) :
	# 		print 'Sending: ' + l
	# 		s.write(l + '\n') # Send g-code block
	# 		grbl_out = s.readline() # Wait for response with carriage return
	# 		print ' : ' + grbl_out.strip()
	 
	# # Wait here until printing is finished to close serial port and file.
	# raw_input("  Press <Enter> to exit.")
	 
	# # Close file and serial port
	# f.close()
	# s.close()