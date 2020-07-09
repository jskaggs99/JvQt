# serial2marlin
"""
Will take care of sending G-code through serial to Marlin. 

"""
import serial
import time

time.sleep(2)



def send2marlin(text COM = 'COM6', baudrate = 115200, *args, **kwargs):
	""" 
	Sends G-Code as an input into Marlin. Removes the need for pronterface.
	"""
	# try:
	# 	
	# 	continue
	# except
	# 	
	ser = serial.Serial(COM, baudrate) 
	ser.write(b'' + text + '\n')
	# ser.write(b'G28 X0\n') # My second issue comes up when I'm not sure of the line ending character that the M2 expects (maybe \n, \r or even \r\n)
	ser.close()


class xystage():
	connection_dict = {'xstepper': {'COM': 'ASRL3::INSTR', 'connection':None, 'movementhistory': None, 'homed': False}
                       'ystepper': {'COM': 'ASRL3::INSTR', 'connection':None, 'movementhistory': None, 'homed': False},
						}

class zprobe():

	def lift_down():
		send2marlin(G0Z5)
		


def manualgcodesender():

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