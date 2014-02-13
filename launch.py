import watchman, oldwatchman
from PySide import QtGui, QtCore

window_w = 800
window_h = 600

class SPApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SPApp, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        #geo = QtGui.QDesktopWidget().availableGeometry()
        self.resize(window_w, window_h)
        self.center()
        self.setWindowTitle('SeePlay')

        # SETTING THE SCENE        
        leftbg = QtGui.QLabel(self)
        leftbg.resize(window_w*0.25,window_h)
        leftbg.move(0,0)
        leftbg.setStyleSheet("QLabel { background-color: #333333; color: #EEEEEE; }")
        
        rightbg = QtGui.QLabel(self)
        rightbg.resize(window_w*0.75,window_h)
        rightbg.move(window_w*0.25,0)
        rightbg.setStyleSheet("QLabel { background-color: #666666; color: #EEEEEE; }")
        
        title = QtGui.QLabel(self)
        title.resize(window_w*0.25,35)
        title.move(0,0)
        title.setText('SeePlay')
        title.setStyleSheet("QLabel { padding: 5px; font-size: 20px; text-align: center; background-color: rgba(100, 100, 100, 100); color: #DEDEDE; }")

        # INTERACTIVE CONTROLS
        dens = QtGui.QLineEdit(self)
        dens.resize(60,30)
        dens.move(130, 40)
        dens.setText('64')

        oldwatchbtn = QtGui.QPushButton('Old school sampling', self)
        oldwatchbtn.setToolTip('This is a holdup')
        oldwatchbtn.resize(120,30)
        oldwatchbtn.move(5, 40)
        oldwatchbtn.clicked.connect(lambda: self.launch_old_watch(int(dens.text())))
        
        watchbtn = QtGui.QPushButton('SimpleCV', self)
        watchbtn.setToolTip('This is a holdup')
        watchbtn.resize(120,30)
        watchbtn.move(5, 75)
        watchbtn.clicked.connect(lambda: self.launch_watch())

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def launch_old_watch(self, dens):
        geo = QtGui.QDesktopWidget().availableGeometry()
        self.watch = QtGui.QMainWindow()
        self.watch.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.watch.setFixedSize(geo.width() / 2, geo.height() / 2)
        self.watch.setWindowTitle(self.tr('Dem Colorz'))
        self.watchpanel = oldwatchman.WatchWindow(dens, self)
        self.watch.setCentralWidget(self.watchpanel)
        self.watch.show()
        
    def launch_watch(self):
        watchman.start_watching()
