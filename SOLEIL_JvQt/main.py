# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import numpy as np


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('SOLEIL_JvQt.ui', self)
#        self.keithley_checkbox = self.findChild(QtWidgets.QCheckBox,'checkBox_Keithley')

        chk =  self.checkBox_Keithley
        if chk.isChecked():
            print('keithley checkbox is check\n')
#        # Create a sin wave
#        x_time = np.arange(0, 100, 0.1);
#        y_amplitude = np.sin(x_time)

#        pltSignal = self.plottedData_pixel1
#        pltSignal.clear()
#        pltSignal.setLabel('left', 'Signal Sin Wave', units ='(V)')
#        pltSignal.setLabel('bottom', 'Time', units ='(sec)')
#        pltSignal.plot(x_time, y_amplitude, clear = True)

        self.ui.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

main()

#if __name__ == '__main__':
#    main()
