from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pyqtgraph import PlotWidget
from JvQtUI import Ui_MainWindow
from datetime import datetime
import warnings, visa
import Connection

from random import uniform

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

        # Connection panel - buttons
        self.ui.pushButton_connect.clicked.connect(self.connect_btn)
        self.ui.pushButton_selectDir.clicked.connect(self.select_folder_btn)
        self.ui.pushButton_checkIsc.clicked.connect(self.check_solo_Isc_btn)
        self.ui.pushButton_clear_outputwindow.clicked.connect(lambda: self.clear_message(self.msg_dict['msg']))
# Hitting the "Connect Button
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

            # print('\n Connecting light shutter \n -----------------------------')
            # TODO: incorporate or call light shutter function

            msg += '\n Connecting pixel switch \n -----------------------------'
            # print('\n Connecting pixel switch \n -----------------------------')
            # TODO: incorporate or call pixel switch function
        else:
            self.ui.pushButton_connect.setStyleSheet('background-color: #cb181d') #red
            self.ui.pushButton_connect.setText('Disconnected')
            msg += '\nKeithley connection fail\n'

        self.append_message(msg)
        self.ui.output_window.setText(self.msg_dict['msg'])

    def connect_keithley(self):
        self.connection_dict['keithley_parm']['connection'] = Connection.Connect()
        try:
            keithley_rs.keithley_cnt(self.connection_dict['rm'],self.connection_dict['keithley_parm']['COM'])
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

    def list_connected_devices(self):
        rm_list = self.rm.list_resources()
        msg = ''
        for r_ in rm_list:
            msg += r_ + '\n'
        self.append_message(msg)
        self.ui.output_window.setText(self.msg_dict['msg'])

    def append_message(self, msg):
        self.msg_dict['msg'] += msg + '\n'

    def clear_message(self, msg):
        self.msg_dict['msg'] = ''
        self.ui.output_window.setText(self.msg_dict['msg'])

    def autoScroll(self):
        vsb = self.ui.output_window.verticalScrollBar()
        if vsb.value() <= vsb.maximum():
            vsb.setValue(vsb.value() + 2)# ERROR!!!

    def output_text(self, str):
        self.append_message(str)
        self.ui.output_window.setText(self.msg_dict['msg'])
        #self.autoScroll()

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
        self.append_message(msg)
        self.ui.output_window.setText(self.msg_dict['msg'])
        # filepath = os.path.join(savedir, filename)

        # IS RETURN NECCESSARY?
        # return filepath

    def check_solo_Isc_btn(self):
        value = uniform(0, .0015)
        self.ui.label_checkedIsc.setText(str(round(value,4)))
        msg = 'Isc: ' + str(value) + '\n'
        self.output_text(msg)

    # def create_save_txt(self): 

    # def cnt_keithley(self):
    #     if self.ui.checkBox_Keithley.isClicked:

    #
    #
    # def cnt_lightShutter(self):
    #
    #
    # def cnt_pixelSwitch(self):
