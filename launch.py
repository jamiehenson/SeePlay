import watchman, oldwatchman
from PySide import QtGui, QtCore

window_w = 640 
window_h = 480

class SPApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SPApp, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.center()
        self.setWindowTitle('SeePlay')
        self.setFixedSize(window_w, window_h)
        
        boxheight = 30

        # SETTING THE SCENE        
        leftbg = QtGui.QLabel(self)
        leftbg.resize(window_w*0.33,window_h)
        leftbg.move(0,0)
        leftbg.setStyleSheet("QLabel { background-color: #333333; color: #EEEEEE; }")
        
        rightbgtop = QtGui.QLabel(self)
        rightbgtop.resize(window_w*0.68,window_h)
        rightbgtop.move(window_w*0.33,0)
        rightbgtop.setStyleSheet("QLabel { background-color: #666666; color: #EEEEEE; }")
        
        rightbgbtm = QtGui.QLabel(self)
        rightbgbtm.resize(window_w*0.68,window_h)
        rightbgbtm.move(window_w*0.33,window_h*0.5)
        rightbgbtm.setStyleSheet("QLabel { background-color: #666666; color: #EEEEEE; }")
        
        title = QtGui.QLabel(self)
        title.resize(window_w*0.33,35)
        title.move(0,0)
        title.setText('SeePlay')
        title.setStyleSheet("QLabel { padding: 5px; font-size: 20px; text-align: center; background-color: rgba(100, 100, 100, 100); color: #EFEFEF; }")
        
        # INTERACTIVE CONTROLS     
        termout = QtGui.QTextEdit(self)
        termout.resize(window_w*0.33-10,window_h*0.7)
        termout.move(5,boxheight+10)
        termout.setReadOnly(True)

        oldwatchbtn = QtGui.QPushButton('Old school sampling', self)
        oldwatchbtn.resize(window_w*0.33-10,boxheight)
        oldwatchbtn.move(5, window_h-(3*boxheight)-5)
        oldwatchbtn.clicked.connect(lambda: self.launch_old_watch(64))
        
        watchbtn = QtGui.QPushButton('LAUNCH', self)
        watchbtn.resize(window_w*0.33-10,2*boxheight)
        watchbtn.move(5, window_h-(2*boxheight)-5)
        watchbtn.clicked.connect(lambda: self.launch_watch())
        
        # RIGHT BUTTONS
        # VISUAL SETTINGS
        stitle = QtGui.QLabel(self)
        stitle.resize(window_w*0.68,boxheight)
        stitle.move(window_w*0.33,0)
        stitle.setText('Visual options')
        stitle.setStyleSheet("QLabel { padding: 5px; font-size: 18px; text-align: center; background-color: rgba(200, 200, 200, 150); color: #333333; }")
        
        # Look out for
        inputsrc = QtGui.QLabel(self)
        inputsrc.resize(window_w*0.16,boxheight)
        inputsrc.move(window_w*0.33, (1 * boxheight) + 5)
        inputsrc.setText('Input source: ')
        inputsrc.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        inputsrcbox = QtGui.QComboBox(self)
        inputsrcbox.resize(window_w*0.5,boxheight)
        inputsrcbox.move(window_w*0.33 + window_w*0.16, 1 * boxheight + 5)
        inputsrcbox.addItem("Screen")
        inputsrcbox.addItem("Camera")
        
        # Look out for
        lookout = QtGui.QLabel(self)
        lookout.resize(window_w*0.16,boxheight)
        lookout.move(window_w*0.33, (2 * boxheight) + 5)
        lookout.setText('Look out for: ')
        lookout.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        lookoutbox = QtGui.QComboBox(self)
        lookoutbox.resize(window_w*0.5,boxheight)
        lookoutbox.move(window_w*0.33 + window_w*0.16, (2 * boxheight) + 5)
        lookoutbox.addItem("Faces")
        lookoutbox.addItem("Colours (scenery)")
        lookoutbox.addItem("Movement")
        
        # AUDIO SETTINGS
        stitle2 = QtGui.QLabel(self)
        stitle2.resize(window_w*0.68,boxheight)
        stitle2.move(window_w*0.33, (4 * boxheight) + 5)
        stitle2.setText('Audio options')
        stitle2.setStyleSheet("QLabel { padding: 5px; font-size: 18px; text-align: center; background-color: rgba(200, 200, 200, 150); color: #333333; }")
                
        # Band type
        band = QtGui.QLabel(self)
        band.resize(window_w*0.16,boxheight)
        band.move(window_w*0.33, (5 * boxheight) + 10)
        band.setText('Band type: ')
        band.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        bandbox = QtGui.QComboBox(self)
        bandbox.resize(window_w*0.5,boxheight)
        bandbox.move(window_w*0.33 + window_w*0.16, (5 * boxheight) + 10)
        bandbox.addItem("Solo piano")
        bandbox.addItem("Jazz trio")
        bandbox.addItem("Electronic")
        bandbox.addItem("Orchestra")
        
        # Time sig
        sig = QtGui.QLabel(self)
        sig.resize(window_w*0.16,boxheight)
        sig.move(window_w*0.33, (6 * boxheight) + 10)
        sig.setText('Time signature: ')
        sig.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        sigbox = QtGui.QComboBox(self)
        sigbox.resize(window_w*0.5,boxheight)
        sigbox.move(window_w*0.33 + window_w*0.16, (6 * boxheight) + 10)
        sigbox.addItem("4/4")
        sigbox.addItem("3/4")
        sigbox.addItem("5/4")
        
        # Tempo
        musictime = QtGui.QLabel(self)
        musictime.resize(window_w*0.16,boxheight)
        musictime.move(window_w*0.33, (7 * boxheight) + 10)
        musictime.setText('Tempo: ')
        musictime.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        musictimebox = QtGui.QComboBox(self)
        musictimebox.resize(window_w*0.5,boxheight)
        musictimebox.move(window_w*0.33 + window_w*0.16, (7 * boxheight) + 10)
        musictimebox.addItem("Slow (80 bpm)")
        musictimebox.addItem("Normal (120 bpm)")
        musictimebox.addItem("Fast (160 bpm)")

        # CREDZ
        stitle2 = QtGui.QLabel(self)
        stitle2.resize(160,26)
        stitle2.move(window_w-stitle2.width(),window_h-stitle2.height())
        stitle2.setText('SeePlay by Jamie Henson, 2014')
        stitle2.setStyleSheet("QLabel { padding: 2px; font-size: 10px; text-align: right; color: #CCCCCC; }")

        self.show()
        
    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize() 

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
