import warnings, visa


class Connect():
    def __init__(self):
        self.inst = None
        self.rm = None
        self.com_port = None
        self.fncts = None
        
    def keithley_cnt(self,rm,com_port):
        inst = rm.open_resource(com_port)
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        self.rm = rm
        self.com_port = com_port
        self.inst = inst
        self.Keithley = Keithley(self)
        
    def pixelswitch_cnt(self,rm,com_port):
        inst = rm.open_resource(com_port)
        self.rm = rm
        self.com_port = com_port
        self.inst = inst
        self.Pixelswitch = Pixelswitch(self)
    
    def shutter_cnt(self,rm,com_port):
        inst = rm.open_resource(com_port)
        self.rm = rm
        self.com_port = com_port
        self.inst = inst
        self.Shutter = Shutter(self)
    
    def get_inst(self):
        return self.inst

    def close_inst(self):
        self.inst.close()
        self.inst = None


class Pixelswitch(object):
    def __init__(self,cnt):
        self.inst = cnt.inst
    def turn_on_pixel(self, pixelval):
        self.inst.write(str(pixelval))
        msg = self.inst.read()
        print(msg)

    def turn_off_all(self):
        self.inst.write(str(0))
        msg = self.inst.read()
        print(msg)


class Shutter(object):
    def __init__(self,cnt):
        self.inst = cnt.inst
    def shutter_open(self):
        self.inst.write(str(2))
        print('Light shutter open\n')

    def shutter_close(self):
        self.inst.write(str(1))
        print('Light shutter close \n')


class Keithley(object):
    def __init__(self,cnt):
        self.inst = cnt.inst
    def inst_set_volt_source_mode(self):
        self.inst.write_inst(":SOUR:FUNC VOLT")
        print('Set voltage as source')

    def inst_set_curr_source_mode(self):
        self.inst.write_inst(":SOUR:FUNC CURR")
        print('Set current as source')

    def inst_set_curr_sense_dc_mode(self):
        self.inst.write_inst(":SENSE:FUNC 'CURR:DC'")
        print('DC current sensing')

    def inst_set_volt_sense_dc_mode(self):
        self.inst.write_inst(":SENSE:FUNC 'VOLT:DC'")
        print('DC voltage sensing')

    def inst_set_volt_lim(self, limit):
        write_msg = ":SENS:VOLT:PROT %f" % limit
        self.inst.write_inst(write_msg)
        print('Set voltage compliance to %fV' % limit)

    def inst_set_curr_lim(self, limit):
        write_msg = ":SENSE:CURR:PROT %f" % limit
        self.inst.write_inst(write_msg)
        print('Set current compliance to %fA' % limit)

    def inst_set_volt_sweep_mode(self):
        self.inst.write_inst(":SOUR:VOLT:MODE FIX")
        print('Set voltage source sweep mode')

    def inst_set_source_delay_time(self, delay_time):
        write_msg = ":SOUR:DEL %f" % delay_time
        self.inst.write_inst(write_msg)
        print('Set source delay time %f second' % delay_time)

    def inst_curr_mode_fix(self):
        self.inst.write_inst(":SOUR:CURR:MODE FIXED")
        print('Fix current sensing mode')

    def inst_collct_data_format(self):
        self.inst.write_inst(":FORM:ELEM CURR,VOLT,TIME")
        print('Select data collecting item format to be current')

    #    def inst_collct_volt_format(self):
    #        self.inst.write(":FORM:ELEM VOLT")
    #        print('Select data collecting item format to be voltage')

    def inst_set_source_volt_value(self, voltage):
        self.inst.write_inst(":SOUR:VOLT %f" % voltage)

    def inst_4wire(self):
        self.inst.write_inst(":SYST:RSEN ON")
        print('Mode: 4-wire measurement')

    def inst_2wire(self):
        self.inst.write_inst(":SYST:RSEN OFF")
        print('Mode: 2-wire measurement')

    def inst_output_on(self):
        self.inst.write_inst(":OUTP ON")
        print("Output on")

    def inst_output_off(self):
        self.inst.write_inst(":OUTP OFF")
        print("Output off")

    def inst_reset(self):
        self.inst.write_inst("*RST")
        print('Reset GPIB (keithley) connection')

    def inst_set_high_impedance(self):
        self.inst.write_inst(":OUTP:SMOD HIMP")
        print('Set high impedance mode')

    def inst_concurrent_off(self):
        self.inst.write_inst(":SENS:FUNC:CONC OFF")
        print('Turn off concurrent functions')

    def inst_front_connct(self):
        self.inst.write_inst(":ROUT:TERM FRONT")
        print('Set I/O to front connectors')

    def current_sensing(self, cmpl_current, query_time):
        self.setting_init()
        self.inst_set_volt_source_mode()
        self.inst_set_curr_sense_dc_mode()
        self.inst_set_curr_lim(cmpl_current)
        self.inst_set_volt_sweep_mode()
        self.inst_collct_data_format()
        self.inst_set_source_delay_time(query_time)
        self.inst_4wire()

    def voltage_sensing(self, cmpl_volt, query_time):
        self.setting_init()
        self.inst_set_curr_source_mode()
        self.inst_set_volt_sense_dc_mode()
        self.inst_curr_mode_fix()
        self.inst_set_volt_lim(cmpl_volt)
        self.inst_set_source_delay_time(query_time)
        self.inst_collct_data_format()
        self.inst_4wire()

    def setting_init(self):
        self.inst_reset()
        self.inst_front_connct()
        self.inst_set_high_impedance()
        self.inst_concurrent_off()


