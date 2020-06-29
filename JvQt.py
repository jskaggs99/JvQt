import os, sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from JvQtFuncs import Func_MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = Func_MainWindow()
    gui.window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
   main()


   # def __init__(self, *args, **kwargs):
   #     super(Ui_MainWindow, self).__init__(*args, **kwargs)