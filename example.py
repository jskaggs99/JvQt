import visa, Connection
import numpy as np

rm = visa.ResourceManager()
keithley_com_port = 'GPIB2::20::INSTR'
shutter_com_port = 'ASRL3::INSTR'
pixelswitch_com_port = 'ASRL5::INSTR'

keithley_cnt = Connection.Connect()
keithley_cnt.keithley_cnt(rm,keithley_com_port)

shutter_cnt = Connection.Connect()
shutter_cnt.shutter_cnt(rm,shutter_com_port)

pixelswitch_cnt = Connection.Connect()
pixelswitch_cnt.pixelswitch_cnt(rm,pixelswitch_com_port)


## Example of taking JV measurement of each pixel

# setup keithley to measure current at for a given voltage
cmplA = 0.002  # 2 mA, compliance current
src_sec = 0.05 # 50 ms, source delay time
keithley_cnt.Keithley.current_sensing(cmplA,src_sec) # setup keithley to be current sensing mode
keithley_cnt.Keithley.inst_output_on()  # turn on OUTPUT on keithley

# define voltage range
vmin = -0.1  # unit in V
vmax = 1.2   # unit in V
pts = 200   # number of points
voltage_arr = np.linspace(vmin,vmax,pts)   # voltage array

# pixel index, define the pixel that we would like to measure JV
pixel_index = np.arange(1,7)

# initialize an array (list) to store measured current
current_arr = [[]]

# turn on light shutter, expose device to 1-Sun
shutter_cnt.Shutter.shutter_open()

# measure JV for individual pixel in a loop
for p_ in pixel_index:
    pixelswitch_cnt.Pixelswitch.turn_on_pixel(pixelval=p_)  # turn on pixel p_
    for v_ in voltage_arr:
        current_arr.append(keithley_cnt.Keithley.inst_set_source_volt_value(voltage=v_))

shutter_cnt.Shutter.shutter_close()
pixelswitch_cnt.Pixelswitch.turn_off_all()
keithley_cnt.Keithley.inst_output_off()

