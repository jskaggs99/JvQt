#!/usr/bin/env python
# coding: utf-8

import visa
import Connection
import matplotlib.pyplot as plt
import numpy as np

class connection_setup:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.cmpl_current = 0.002   # default value 0.002A
        self.cmpl_voltage = 2.0     # default value is 2V
        self.query_time = 0.2       # default query time is 0.2 sec    
        self.keithley = None
        self.pixelswitch = None
        self.shutter = None
    
    def keithley_cmpl_current(self,cmpl_current):
        self.cmpl_current = cmpl_current
    
    def keithley_query_time(self,query_time):
        self.query_time = query_time
        
    def keithley_cmpl_voltage(self,cmpl_voltage):
        self.cmpl_voltage = cmpl_voltage

    def cnnct_keithley(self,gpib_name):
        keithley = Connection.keithley()
        keithley._init_(self.rm)
        keithley.open_gpib(gpib_name)
        self.keithley = keithley

    def cnnct_pixelswitch(self,arduino_name):
        pixelswitch = Connection.pixelswitch()
        pixelswitch._init_(self.rm)
        pixelswitch.open_pixelswitcher_connection(arduino_name)
        self.pixelswitch = pixelswitch
        
    def cnnct_shutter(self,shutter_name):
        shutter = Connection.shutter()
        shutter._init_(self.rm)
        shutter.open_shutter_connection(shutter_name)
        self.shutter = shutter
        
    def connect(self,gpib_name=None, pixel_com_name=None, shutter_com_name=None):
        if gpib_name is not None:
            self.cnnct_keithley(gpib_name)
        if pixel_com_name is not None:
            self.cnnct_pixelswitch(pixel_com_name)
        if shutter_com_name is not None:
            self.cnnct_shutter(shutter_com_name)
        

    def get_voc(self):
        self.keithley.voltage_sensing(self.cmpl_voltage,self.query_time)
        self.keithley.inst_output_on()
        self.shutter.shutter_open()
        data = np.array(self.keithley.get_inst().read().split(','),dtype='float')
        voc = data[0]
        self.keithley.inst_output_off()
        self.shutter.shutter_close()
        print(data)
        print('Voc is %f V'%voc)
        return voc

    def get_isc(self):
        self.keithley.current_sensing(self.cmpl_current,self.query_time)
        self.keithley.inst_output_on()
        self.shutter.shutter_open()
        self.keithley.inst_set_source_volt_value(0)
        data = np.array(self.keithley.get_inst().read().split(','),dtype='float')
        isc = data[1]
        self.keithley.inst_output_off()
        self.shutter.shutter_close()
        print(data)
        print('Isc is %f A'%isc)
        return isc

    def voltage_sweep(self,volt_arr):
        data = np.empty((volt_arr.size,3))
        self.keithley.current_sensing(self.cmpl_current,self.query_time)
        self.keithley.inst_output_on()
        for index,_v in enumerate(volt_arr):
            self.keithley.inst_set_source_volt_value(_v)
            output = np.array(self.keithley.get_inst().read().split(','),dtype='float')
            data[index,:] = np.array(output[:])
        self.keithley.inst_output_off()
        return data

    def spo(vapp,time_length,time_interval,fid):
        start_time = time.time()
        self.keithley.current_sensing(self.cmpl_current,self.query_time)
        self.keithley.inst_output_on()
        self.keithley.inst_set_source_volt_value(vapp)
        while (time.time() - start_time) < time_length:
            output = np.array(self.keithley.get_inst().read().split(','),dtype='float')
            fid.write(output)
            time.sleep(time_interval)
        self.keithley.inst_output_off()




