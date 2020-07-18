from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pyqtgraph import PlotWidget
from JvQtUI import Ui_MainWindow
from datetime import datetime
import warnings, visa
import Connection
# import movement
# import savewrite
import serial2marlin

from random import uniform #just since hardware connections not etablished

"""
==========GOALS============
Set Automation page to select cell and light up in blue, and display order of it being scanned
Place image in top left and also .exe icon
Create .exe file
"""

class Func_MainWindow():
    connection_dict = {'keithley_parm': {'cmplV': 2, 'cmplA': 0.002, 'src_sec': 0.2, 'sens_sec': 0.2, 'src_mode': 'V',
                                         'sens_mode': 'I', 'v_min': 0.0, 'v_max': 1.0, 'delta_v': 0.05,
                                         'COM': 'GPIB2::20::INSTR','connection':None, 'chbx_state': True,
                                         'state': True},
                       'shutter_parm': {'COM': 'ASRL3::INSTR', 'connection':None, 'chbx_state': True, 'state': True,
                                        'Position': 'OFF'},
                       'px_swtch_parm': {'COM': 'ASRL5::INSTR', 'connection':None, 'chbx_state': True, 'pix_on': None,
                                         'pix_mtype': None},
                       'marlin_driverboard': {'COM': 'COM5', 'baudrate': 115200, 'connection': None},                   
                       'rm':visa.ResourceManager()}

    msg_dict = {'msg':''}

    def __init__(self, *args, **kwargs):
        # Initiating GUI window
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow=self.window)

        # Update GUI with open time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.ui.current_time_label.setText(dt_string)

        # Connection panel - preset checkbox conditions
        self.ui.checkBox_Keithley.setChecked(True)
        self.ui.checkBox_lightShutter.setChecked(True)
        self.ui.checkBox_pixelSwitch.setChecked(True)

        # List all the connected device in the output window
        self.rm = visa.ResourceManager()
        self.list_connected_devices()

        # Save directory
        # self.fillallentries = True

        # Initialization panel - buttons
        self.ui.pushButton_connect.clicked.connect(self.connect_btn)
        self.ui.pushButton_shutter.clicked.connect(self.shutter_btn)
        self.ui.pushButton_selectDir.clicked.connect(self.select_folder_btn)
        self.ui.pushButton_checkIsc.clicked.connect(self.check_solo_Isc_btn)
        self.ui.pushButton_checkVoc.clicked.connect(self.check_solo_Voc_btn)
        self.ui.pushButton_checkallIsc.clicked.connect(self.check_all_Isc_btn)
        self.ui.pushButton_checkallVoc.clicked.connect(self.check_all_Voc_btn)
        self.ui.pushButton_clear_outputwindow.clicked.connect(lambda: self.clear_message(self.msg_dict['msg']))

        # Automation panel - constants
        self.number_of_cells = 30 # Default value. 

        # Automation panel - buttons
        self.ui.pushButton_selectall.clicked.connect(lambda: self.selectall(True))
        self.ui.pushButton_deselectall.clicked.connect(lambda: self.selectall(False))
        self.ui.pushButton_auto_run.clicked.connect(self.run_automated_scans)
        self.ui.pushButton_connectMarlin.clicked.connect(self.connectMarlin)
        self.ui.pushButton_closeMarlin.clicked.connect(self.closeMarlin)
        self.ui.pushButton_sendmarlin.clicked.connect(self.sendgcode)
        for i in range(self.number_of_cells): # Sets all of the cell buttons to be clickable. 
            cell_label_auto = 'pushButton_cell1_' + str(i+1)  
            button = getattr(self.ui, cell_label_auto)
            button.setCheckable(True)

        # Automation Connection
        self.serialport = None

############################
##   Output window text   ##
############################

    def append_message(self, msg):
        self.msg_dict['msg'] += msg + '\n'

    def autoScroll(self):
        vsb = self.ui.output_window.verticalScrollBar()
        if vsb.value() <= vsb.maximum():
            vsb.setValue(vsb.value() + 2)# ERROR!!!

    def output_text(self, str):
        self.append_message(str)
        self.ui.output_window.setText(self.msg_dict['msg'])

    def clear_message(self, msg):
        self.msg_dict['msg'] = ''
        self.ui.output_window.setText(self.msg_dict['msg'])
        #self.autoScroll()

#======================================================================================================================================
#   Initialization (Page 1 of 5)
#======================================================================================================================================

############################
## Hardware Connections   ##
############################

    def connect_btn(self):
        now = datetime.now() # Displays the time the connect button was pressed
        current_time = now.strftime('%H:%M:%S')

        msg = 'Connecting keithley 2401 \n ----------------------------- \n'

        self.update_keithley_parm() # Gathers all of the parameters from function
        for k, v in self.connection_dict['keithley_parm'].items(): msg += k + ': ' + str(v) + '\n'

        self.ui.label_timeClickCntBnt.setText(current_time)

        if self.connect_keithley() == 1:
            msg += '\nKeithley connection success'
            msg += '\n Connecting light shutter \n -----------------------------'
            self.ui.pushButton_connect.setStyleSheet('background-color: #a1d99b') # green
            self.ui.pushButton_connect.setText('Connected')

            msg += '\n Connecting light shutter \n -----------------------------'
            # print('\n Connecting light shutter \n -----------------------------')
            # TODO: incorporate or call light shutter function

            msg += '\n Connecting pixel switch \n -----------------------------'
            # print('\n Connecting pixel switch \n -----------------------------')
            # TODO: incorporate or call pixel switch function
        else:
            self.ui.pushButton_connect.setStyleSheet('background-color: #cb181d') #red
            self.ui.pushButton_connect.setText('Disconnected')
            msg += '\nKeithley connection fail\n'

        self.output_text(msg)

    def shutter_btn(self):

        msg = 'Connecting solar sim shutter \n ----------------------------- \n'

        self.update_shutter_param() # Gathers all of the parameters from function
        for k, v in self.connection_dict['shutter_parm'].items(): msg += k + ': ' + str(v) + '\n'

        if self.connect_shutter() == 1:
            msg += '\nShutter connection success'
            self.ui.pushButton_shutter.setStyleSheet('background-color: #a1d99b') # green
            self.ui.pushButton_shutter.setText('Connected')
            self.ui.label_cntStatus.setText('On')

        else:
            self.ui.pushButton_shutter.setStyleSheet('background-color: #cb181d') #red
            self.ui.pushButton_shutter.setText('Disconnected')
            self.ui.label_cntStatus.setText('Off')
            msg += '\nShutter connection fail\n'

        self.output_text(msg)


    def connect_keithley(self): # Checks the connection between the keithley
        self.connection_dict['keithley_parm']['connection'] = Connection.Connect()
        try:
            keithley_rs.keithley_cnt(self.connection_dict['rm'],self.connection_dict['keithley_parm']['COM'])
            return 1
        except:
            return -1

    def connect_shutter(self): # Checks the connection between the shutter
        self.connection_dict['shutter_parm']['connection'] = Connection.Connect() # Fills the dictionary 
        try:
            shutter_rs.shutter_cnt(self.connection_dict['rm'],self.connection_dict['shutter_parm']['COM'])
            return 1
        except:
            return -1

    def update_keithley_parm(self):
        cmplV = self.ui.lineEdit_cmpl_V.text()
        cmplA = self.ui.lineEdit_cmpl_A.text()
        src_sec = self.ui.lineEdit_srcDelaySec.text()
        sens_sec = self.ui.lineEdit_meaDelaySec.text()
        com_val = self.ui.lineEdit_keithleyCOM.text()
        chbox_val = self.ui.checkBox_Keithley.isChecked()

        parm_list = ['cmplV', 'cmplA', 'src_sec', 'sens_sec']
        parm_val = [cmplV, cmplA, src_sec, sens_sec]
        for parm_, val_ in zip(parm_list, parm_val):
            if len(val_) != 0:
                self.connection_dict['keithley_parm'][parm_] = float(val_)
            else:
                warnings.warn('%s field has empty input' % (parm_))

        parm_list = ['COM', 'chbx_state']
        parm_val = [com_val, chbox_val]
        for parm_, val_ in zip(parm_list, parm_val):
            self.connection_dict['keithley_parm'][parm_] = val_

    def update_shutter_param(self):
        # Gather information from the initialization panel corresponding to shutter
        com_val = self.ui.lineEdit_shutterCOM.text()
        chbox_val = self.ui.checkBox_lightShutter.isChecked()

        parm_list = ['COM', 'chbx_state']
        parm_val = [com_val, chbox_val]
        for parm_, val_ in zip(parm_list, parm_val):
            self.connection_dict['shutter_parm'][parm_] = val_

    def list_connected_devices(self):
        rm_list = self.rm.list_resources()
        msg = ''
        for r_ in rm_list:
            msg += r_ + '\n'
        self.output_text(msg)

############################
##    Saving Process      ##
############################

    def select_folder_btn(self):
        input_dir = QFileDialog.getExistingDirectory(None, caption = 'Select a folder:', options = QFileDialog.ShowDirsOnly)
        self.ui.lineEdit_filePath.setText(input_dir)

    def get_save_loc(self):
        # Pulls data from save information on page 1
        # Maybe can have data be appended to a text file based on the Experiment name. 
        today = datetime.now() # Displays the time the connect button was pressed
        current_day = today.strftime('%Y_%m_%d')

        savedir = self.ui.lineEdit_filePath.text()
        exp_name = self.ui.lineEdit_expt_name.text()
        dev_name =  self.ui.lineEdit_device_name.text()
        filename = current_day + '_' + exp_name + '_' +dev_name 
        msg = '\nFilename: ' + filename + '\n' # saves individual file for each device...
        self.output_text(msg)
        self.savepath = os.path.join(savedir, filename)

    # def create_save_txt(self): 
    def WriteHeader(filename, header):
        savefile = open(filename, 'r')
        # remove any matching 'header' from the file, in case ther are duplicate header rows in the wrong places
        lines = [line for line in file if not line == header]
        file.close()

        # rewrite the file, appending the header to row 1
        file = open(filename, w)
        file.write(''.join([line for line in lines].insert(0,header)))    
        file.close()
    
############################
##   Isc and Voc Check    ##
############################

    def get_Isc(self): # Will need pixel number as an input
        value = uniform(0, .0015)
        return value

    def get_Voc(self):# Will need pixel number as an input
        value = uniform(0, 1.2)
        return value

    def check_solo_Isc_btn(self):
        value = self.get_Isc()
        self.ui.label_checkedIsc.setText(str(round(value,4)))
        msg = 'Isc: ' + str(value) + '\n'
        self.output_text(msg)

    def check_solo_Voc_btn(self):
        value = self.get_Voc()
        self.ui.label_checkedVoc.setText(str(round(value,4)))
        msg = 'Voc: ' + str(value) + '\n'
        self.output_text(msg)

    def check_all_Isc_btn(self):
        nop = 6 # number of pixels on multiplexer board
        pixel_list_int = [x+1 for x in list(range(nop))] # Creates a list [1,2,3,4,5,6]
        pixel_list_str = ['label_pixel'+str(i)+'_Isc' for i in pixel_list_int] # newlist = ['label_pixel1_Isc', 'label_pixel2_Isc',...]
        pixels = self.pixelselected() # Calls other function to retrieve Bool list which checkbox_pixels were selected [True, True, True, False, ...]
        for i in pixel_list_int:
            if pixels[i-1] == True:
                value = self.get_Isc()
                textbox = getattr(self.ui, pixel_list_str[i-1])
                textbox.setText(str(round(value,4)))
                msg = pixel_list_str[i-1][6:] + ' : ' + str(value) + '\n'
                self.output_text(msg)

    def check_all_Voc_btn(self):
        nop = 6 # number of pixels on multiplexer board
        pixel_list_int = [x+1 for x in list(range(nop))] # Creates a list [1,2,3,4,5,6]
        pixel_list_str = ['label_pixel'+str(i)+'_Voc' for i in pixel_list_int] # newlist = ['label_pixel1_Isc', 'label_pixel2_Isc',...]
        pixels = self.pixelselected() # Calls other function to retrieve Bool list which checkbox_pixels were selected [True, True, True, False, ...]
        for i in pixel_list_int:
            if pixels[i-1] == True:
                value = self.get_Voc()
                textbox = getattr(self.ui, pixel_list_str[i-1])
                textbox.setText(str(round(value,4)))
                msg = pixel_list_str[i-1][6:] + ' : ' + str(value) + '\n'
                self.output_text(msg)

    def pixelselected(self):
        chbox_val1 = self.ui.checkBox_pixel1.isChecked()
        chbox_val2 = self.ui.checkBox_pixel2.isChecked()
        chbox_val3 = self.ui.checkBox_pixel3.isChecked()
        chbox_val4 = self.ui.checkBox_pixel4.isChecked()
        chbox_val5 = self.ui.checkBox_pixel5.isChecked()
        chbox_val6 = self.ui.checkBox_pixel6.isChecked()
        selectedpixels = [chbox_val1, chbox_val2, chbox_val3, chbox_val4, chbox_val5, chbox_val6]
        return selectedpixels 

############################
## Populating Pixel Info  ##
############################
    
    # Either set to have all boxes populate when typed in the first one, or have every pixel greyed out so only the first column matters.


    # def cnt_keithley(self):
    #     if self.ui.checkBox_Keithley.isClicked:

    #
    #
    # def cnt_lightShutter(self):
    #
    #
    # def cnt_pixelSwitch(self):

#======================================================================================================================================
#   JV Automator (Page 3 of 5)
#======================================================================================================================================
    def profilesettings(self):
        t = 5

    def jvprofile(self, number_of_cells):
        for i in number_of_cells:
            self.ui.pushButton_connect.setStyleSheet('background-color: #cb181d') #red

    def selectall(self, Bool):
        for i in range(self.number_of_cells):
            cell_label_auto = 'pushButton_cell1_' + str(i+1)  
            button = getattr(self.ui, cell_label_auto)
            button.setChecked(Bool)

    def find_activated_cells(self):
        noc = self.number_of_cells
        scan_these_cells = []
        for i in range(noc):
            cell_label_auto = 'pushButton_cell1_' + str(i+1)  
            button = getattr(self.ui, cell_label_auto)
            if button.isChecked() == True:
                scan_these_cells.append(True) 
            else:
                scan_these_cells.append(False)
        print(scan_these_cells)
        return scan_these_cells

    def run_automated_scans(self):
        scan_these_cells = self.find_activated_cells()
        if solarcelltray.homed == True:
            for device_ in self.number_of_cells:
                output_text('Now scanning device ' + str(device_))
                movement.move_to(solarcelltray.x,solarcelltray.y)
                movement.measure_JV(solarcelltray.vmax, vmin, pts)
        else:
            output_text('Stage is not homed.')
            
    def connectMarlin(self):
        try:
            self.serialport = serial2marlin.SerialConnect(COM = 'COM5') # Create a object from class
            ser = self.serialport.openserial() # open serial connection using class functions 
            self.ui.pushButton_connectMarlin.setStyleSheet('background-color: #a1d99b') # green
            self.ui.pushButton_connectMarlin.setText('Connected')
            self.output_text('Connected to Marlin.')
            print(ser) # troulbeshooting

        except:
            self.ui.pushButton_connectMarlin.setStyleSheet('background-color: #cb181d') #red
            self.ui.pushButton_connectMarlin.setText('Disconnected')
   
    def closeMarlin(self):
        self.serialport.closeserial()
        self.ui.pushButton_connectMarlin.setStyleSheet('background-color: #FF9999') #red
        self.ui.pushButton_connectMarlin.setText('Closed')
        self.output_text('Closed communication to Marlin')

    def sendgcode(self):
        # ser = self.connection_dict['marlin_driverboard']['connection']
        try:
            text = self.ui.textEdit_manualgcode.toPlainText() # Reads what was typed in the text box
            self.serialport.send2marlin(text)
        # except portNotOpenError:
        #     print('Port is not open. Reopen the port by connecting again')
        #     self.output_text('Port is not open. Reopen the port by connecting again')
        except:
            self.output_text('Call for help')

    def flushbuffer(self):
        # Use when errors occuring
        self.serialport.flushbuffer()
        
