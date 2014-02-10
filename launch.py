import watchman
from PySide import QtGui, QtCore


class SPApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SPApp, self).__init__(parent)
        self.initUI()

    def initUI(self):
        geo = QtGui.QDesktopWidget().availableGeometry()
        self.resize(geo.width() / 2, geo.height() / 2)
        self.center()
        self.setWindowTitle('SeePlay')

        dens = QtGui.QLineEdit(self)
        dens.resize(100,30)
        dens.move(50, 80)

        menu = self.menuBar().addMenu(self.tr('View'))
        action = menu.addAction(self.tr('Live colour feed'))
        action.triggered.connect(lambda: self.launchWatch(int(dens.text())))

        watchbtn = QtGui.QPushButton('GIMP', self)
        watchbtn.setToolTip('This is a holdup')
        watchbtn.resize(100,30)
        watchbtn.move(50, 50)
        watchbtn.clicked.connect(lambda: self.launchWatch(int(dens.text())))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def launchWatch(self, dens):
        geo = QtGui.QDesktopWidget().availableGeometry()
        self.watch = QtGui.QMainWindow()
        self.watch.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.watch.setFixedSize(geo.width() / 2, geo.height() / 2)
        self.watch.setWindowTitle(self.tr('Dem Colorz'))
        self.watchpanel = watchman.WatchWindow(dens, self)
        self.watch.setCentralWidget(self.watchpanel)
        self.watch.show()
