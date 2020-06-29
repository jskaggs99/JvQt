from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
from JvQtUI import Ui_MainWindow
from datetime import datetime
import warnings, visa
import Connection


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

        # Connection panel - buttons
        self.ui.pushButton_connect.clicked.connect(self.connect_btn)

    def connect_btn(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        msg = '\nConnecting keithley 2401 \n ----------------------------- \n'
        # print('\n Connecting keithley 2401 \n -----------------------------')
        self.update_keithley_parm()
        for k, v in self.connection_dict['keithley_parm'].items(): msg += k + ': ' + str(v) + '\n'

        self.ui.label_timeClickCntBnt.setText(current_time)
        if self.connect_keithley() == 1:
            msg += '\nKeithley connection success'
            msg += '\n Connecting light shutter \n -----------------------------'
            # print('\n Connecting light shutter \n -----------------------------')
            # TODO: incorporate or call light shutter function

            msg += '\n Connecting pixel switch \n -----------------------------'
            # print('\n Connecting pixel switch \n -----------------------------')
            # TODO: incorporate or call pixel switch function
        else:
            msg += '\nKeithley connection fail'

        self.ui.pushButton_connect.setStyleSheet('background-color: #a1d99b')

        self.ui.pushButton_connect.setStyleSheet('background-color: #cb181d') #red
        self.ui.output_window.setText(msg)

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
        self.ui.output_window.setText(msg)

    # def cnt_keithley(self):
    #     if self.ui.checkBox_Keithley.isClicked:

    #
    #
    # def cnt_lightShutter(self):
    #
    #
    # def cnt_pixelSwitch(self):
