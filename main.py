import launch
import sys
from PySide import QtGui

def main():
    qapp = QtGui.QApplication(sys.argv)

    sp = launch.SPApp()
    sys.exit(qapp.exec_())

if __name__ == "__main__":
    main()
