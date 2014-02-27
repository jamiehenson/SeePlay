from PySide import QtGui, QtCore
import watchman

window_w = 640 
window_h = 360

class SPApp(QtGui.QMainWindow):

    orch_text = "A light orchestral accompaniment, reacting to colour changes."
    elec_text = "A soft-pad synth accompaniment, reacting to colour changes."
    horr_text = "A highly reactive accompaniment, with orchestral instrumentation."
    sile_text = "A reactive solo piano accompaniment."
    acti_text = "A reactive and frantic orchestral accompaniment."

    user_inputsrc = ""
    user_inputsrcinfo = ""
    user_type = ""
    user_genre = ""
    user_key = ""
    user_mode = ""
    user_tempo = ""
    user_tsig = ""

    def __init__(self):
        super(SPApp, self).__init__()
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
        # termout = QtGui.QTextEdit(self)
        # termout.resize(window_w*0.33-10,window_h*0.7)
        # termout.move(5,boxheight+10)
        # termout.setReadOnly(True)

        watchbtn_slot = 0
        stop_slot = 2

        # oldwatchbtn = QtGui.QPushButton('Old school sampling', self)
        # oldwatchbtn.resize(window_w * 0.33 - 10, boxheight)
        # oldwatchbtn.move(5, ((oldwatchbtn_slot * boxheight) + title.height() + 5))
        # oldwatchbtn.clicked.connect(lambda: self.launch_old_watch(64))

        # showtog = QtGui.QCheckBox("Show CV Window?", self)
        # showtog.resize(window_w*0.33-10, boxheight)
        # showtog.move(5, ((showtog_slot * boxheight) + title.height() + 5) - 5)
        # showtog.setStyleSheet("QCheckBox { padding: 5px; color: #EFEFEF; }")

        watchbtn = QtGui.QPushButton('LAUNCH', self)
        watchbtn.resize(window_w*0.33-10, 2 * boxheight)
        watchbtn.move(5, ((watchbtn_slot * boxheight) + title.height() + 5) - 5)
        watchbtn.clicked.connect(lambda: self.launch_watch())

        stopbtn = QtGui.QPushButton('STOP', self)
        stopbtn.resize(window_w * 0.33 - 10, boxheight * 1.5)
        stopbtn.move(5, ((stop_slot * boxheight) + title.height() + 5) - 5)
        stopbtn.clicked.connect(lambda: self.stop_watch())
        
        # RIGHT BUTTONS
        # VISUAL SETTINGS

        # SLOTS
        visopt_slot = 0
        inputsrc_slot = 1
        inputsrcinfo_slot = 2
        audioopt_slot = 3
        type_slot = 4
        genre_slot = 5
        genreinfo_slot = 6
        key_slot = 7
        mode_slot = 8
        tempo_slot = 9
        tsig_slot = 10
        geninfo_slot = 11

        stitle = QtGui.QLabel(self)
        stitle.resize(window_w*0.68,boxheight)
        stitle.move(window_w*0.33,0)
        stitle.setText('Visual options')
        stitle.setStyleSheet("QLabel { padding: 5px; font-size: 18px; text-align: center; background-color: rgba(200, 200, 200, 150); color: #333333; }")
        
        # Look out for
        inputsrc = QtGui.QLabel(self)
        inputsrc.resize(window_w*0.16,boxheight)
        inputsrc.move(window_w*0.33, (inputsrc_slot * boxheight) + 5)
        inputsrc.setText('Input region: ')
        inputsrc.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")

        self.inputsrcall = QtGui.QPushButton("Whole screen",self)
        self.inputsrcall.resize(window_w*0.175,boxheight)
        self.inputsrcall.move(window_w*0.33 + window_w*0.16, inputsrc_slot * boxheight + 5)
        self.inputsrcall.clicked.connect(lambda: self.set_user_inputsrc("whole"))

        self.inputsrcact = QtGui.QPushButton("Main window",self)
        self.inputsrcact.resize(window_w*0.175,boxheight)
        self.inputsrcact.move(window_w*0.33 + window_w*0.32, inputsrc_slot * boxheight + 5)
        self.inputsrcact.clicked.connect(lambda: self.set_user_inputsrc("active"))

        self.inputsrcreg = QtGui.QPushButton("Region",self)
        self.inputsrcreg.resize(window_w*0.175,boxheight)
        self.inputsrcreg.move(window_w*0.33 + window_w*0.481, inputsrc_slot * boxheight + 5)
        self.inputsrcreg.clicked.connect(lambda: self.set_user_inputsrc("manual"))

        self.inputsrcinfo = QtGui.QLabel("",self)
        self.inputsrcinfo.resize(window_w*0.5,boxheight)
        self.inputsrcinfo.move(window_w * 0.33, inputsrcinfo_slot * boxheight + 5)
        self.inputsrcinfo.setStyleSheet("QLabel { padding: 5px; font-style: italic; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        # AUDIO SETTINGS
        stitle2 = QtGui.QLabel(self)
        stitle2.resize(window_w*0.68,boxheight)
        stitle2.move(window_w*0.33, (audioopt_slot * boxheight) + 10)
        stitle2.setText('Audio options')
        stitle2.setStyleSheet("QLabel { padding: 5px; font-size: 18px; text-align: center; background-color: rgba(200, 200, 200, 150); color: #333333; }")
        
        # Genre
        genre = QtGui.QLabel(self)
        genre.resize(window_w*0.16,boxheight)
        genre.move(window_w*0.33, (genre_slot * boxheight) + 15)
        genre.setText('Genre: ')
        genre.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.genrebox = QtGui.QComboBox(self)
        self.genrebox.resize(window_w*0.5,boxheight)
        self.genrebox.move(window_w*0.33 + window_w*0.16, (genre_slot * boxheight) + 15)
        self.genrebox.addItem("Classical")
        self.genrebox.addItem("Electronic")

        # Genre Info
        self.genreinfo = QtGui.QLabel(self)
        self.genreinfo.resize(window_w*0.68,boxheight)
        self.genreinfo.setText("A light orchestral accompaniment, reacting to colour changes.")
        self.genreinfo.move(window_w*0.33, (genreinfo_slot * boxheight) + 15)
        self.genreinfo.setStyleSheet("QLabel { padding: 5px; font-size: 12px; font-weight: bold; text-align: center; color: #FFFFFF; }")

        # Music type
        mustype = QtGui.QLabel(self)
        mustype.resize(window_w*0.16,boxheight)
        mustype.move(window_w*0.33, (type_slot * boxheight) + 15)
        mustype.setText('Music type: ')
        mustype.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.mustypebox = QtGui.QComboBox(self)
        self.mustypebox.resize(window_w*0.5,boxheight)
        self.mustypebox.move(window_w*0.33 + window_w*0.16, (type_slot * boxheight) + 15)
        self.mustypebox.addItem("Ambient")
        self.mustypebox.addItem("Reactive")

        self.mustypebox.activated[str].connect(lambda: self.switch_genre_box(self.mustypebox.currentText()))
        self.genrebox.activated[str].connect(lambda: self.switch_genre_info_box(self.genrebox.currentText()))

        # Key
        keysig = QtGui.QLabel(self)
        keysig.resize(window_w*0.16,boxheight)
        keysig.move(window_w*0.33, (key_slot * boxheight) + 15)
        keysig.setText('Key: ')
        keysig.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.keysigbox = QtGui.QComboBox(self)
        self.keysigbox.resize(window_w*0.5,boxheight)
        self.keysigbox.move(window_w*0.33 + window_w*0.16, (key_slot * boxheight) + 15)
        self.keysigbox.addItem("C")
        self.keysigbox.addItem("C#")
        self.keysigbox.addItem("D")
        self.keysigbox.addItem("Eb")
        self.keysigbox.addItem("E")
        self.keysigbox.addItem("F")
        self.keysigbox.addItem("F#")
        self.keysigbox.addItem("G")
        self.keysigbox.addItem("Ab")
        self.keysigbox.addItem("A")
        self.keysigbox.addItem("Bb")
        self.keysigbox.addItem("B")
        self.keysigbox.activated[str].connect(lambda: self.set_user_key(self.keysigbox.currentText()))

        # Key
        mode = QtGui.QLabel(self)
        mode.resize(window_w*0.16,boxheight)
        mode.move(window_w*0.33, (mode_slot * boxheight) + 15)
        mode.setText('mode: ')
        mode.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.modebox = QtGui.QComboBox(self)
        self.modebox.resize(window_w*0.5,boxheight)
        self.modebox.move(window_w*0.33 + window_w*0.16, (mode_slot * boxheight) + 15)
        self.modebox.addItem("Major")
        self.modebox.addItem("Minor")
        self.modebox.activated[str].connect(lambda: self.set_user_mode(self.modebox.currentText()))

        # Time sig
        sig = QtGui.QLabel(self)
        sig.resize(window_w*0.16,boxheight)
        sig.move(window_w*0.33, (tsig_slot * boxheight) + 15)
        sig.setText('Time signature: ')
        sig.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.sigbox = QtGui.QComboBox(self)
        self.sigbox.resize(window_w*0.5,boxheight)
        self.sigbox.move(window_w*0.33 + window_w*0.16, (tsig_slot * boxheight) + 15)
        self.sigbox.addItem("3/4")
        self.sigbox.addItem("4/4")
        self.sigbox.addItem("5/4")
        self.sigbox.setCurrentIndex(1)
        self.sigbox.activated[str].connect(lambda: self.set_user_tsig(self.sigbox.currentText()))
        
        # Tempo
        self.tempo = QtGui.QLabel(self)
        self.tempo.resize(window_w*0.16,boxheight)
        self.tempo.move(window_w*0.33, (tempo_slot * boxheight) + 15)
        self.tempo.setText('Tempo: ')
        self.tempo.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.tempobox = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.tempobox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tempobox.resize(window_w*0.5,boxheight)
        self.tempobox.move(window_w*0.33 + window_w*0.16, (tempo_slot * boxheight) + 15)
        self.tempobox.setMinimum(60)
        self.tempobox.setMaximum(180)
        self.tempobox.setValue(120)
        # self.tempobox.setGeometry(30, 40, 100, 30)
        self.tempobox.valueChanged[int].connect(lambda: self.set_user_tempo(self.tempobox.value()))

        # self.tempobox = QtGui.QComboBox(self)
        
        # self.tempobox.addItem("Slow (80 bpm)")
        # self.tempobox.addItem("Normal (120 bpm)")
        # self.tempobox.addItem("Fast (160 bpm)")
        # self.tempobox.setCurrentIndex(1)
        # self.tempobox.activated[str].connect(lambda: self.set_user_tempo(self.tempobox.currentText()))

        # General info
        # geninfo = QtGui.QLabel(self)
        # geninfo.resize(window_w*0.68,boxheight * 4)
        # geninfo.move(window_w*0.33,(geninfo_slot * boxheight) + 20)
        # geninfo.setText('General info ')
        # geninfo.setStyleSheet("QLabel { padding: 5px; font-size: 12px; background-color: rgba(200, 200, 200, 150); color: #FFFFFF; }")

        # CREDZ
        stitle2 = QtGui.QLabel(self)
        stitle2.resize(160,20)
        stitle2.move(window_w-stitle2.width(),window_h-stitle2.height())
        stitle2.setText('SeePlay by Jamie Henson, 2014')
        stitle2.setStyleSheet("QLabel { padding: 2px; font-size: 10px; text-align: right; color: #CCCCCC; }")

        self.set_initial_vars()

        self.show()
        
    def switch_genre_box(self, text):
        self.set_user_type(text)

        if text == "Ambient":
            self.genrebox.clear()
            self.genrebox.addItem("Classical")
            self.genrebox.addItem("Electronic")
            self.genreinfo.setText(self.orch_text)
            self.set_user_genre("Classical")
        else:
            self.genrebox.clear()
            self.genrebox.addItem("Horror")
            self.genrebox.addItem("Silent Movie")
            self.genrebox.addItem("Action")
            self.genreinfo.setText(self.horr_text)
            self.set_user_genre("Horror")

    def switch_genre_info_box(self, text):
        if text == "Classical":
            chosenText = self.orch_text
        elif text == "Electronic":
            chosenText = self.elec_text
        elif text == "Horror":
            chosenText = self.horr_text
        elif text == "Silent Movie":
            chosenText = self.sile_text
        elif text == "Action":
            chosenText = self.acti_text

        self.genreinfo.setText(chosenText)
        self.set_user_genre(text)

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
        if watchman.active == False:
            watchman.active = True
            watchman.start_watching(self)

    def stop_watch(self):
        watchman.active = False
        print "Stopping."

    def set_initial_vars(self):
        print "----------------------------"
        self.set_user_inputsrc("whole")
        self.set_user_type(self.mustypebox.currentText())
        self.set_user_genre(self.genrebox.currentText())
        self.set_user_key(self.keysigbox.currentText())
        self.set_user_mode(self.modebox.currentText())
        self.set_user_tempo(self.tempobox.value())
        self.set_user_tsig(self.sigbox.currentText())
        print "----------------------------"

    def set_user_inputsrc(self, text):
        self.user_inputsrc = text
        self.set_user_inputsrcinfo(text)
        #print "User set input source:", user_inputsrc

    def set_user_inputsrcinfo(self, text):
        if text == "whole":
            chosenText = "Capturing the whole screen."
        elif text == "active":
            chosenText = "Capturing the active window."
        else:
            chosenText = "Capturing a user-defined region: "

        self.user_inputsrcinfo = chosenText
        self.inputsrcinfo.setText(self.user_inputsrcinfo)

        print "Use set input source:", self.user_inputsrcinfo

    def set_user_tempo(self, val):
        self.user_tempo = int(val)
        self.tempo.setText("Tempo: " + str(self.user_tempo))
        print "User set tempo:", self.user_tempo

    def set_user_genre(self, text):
        self.user_genre = text
        print "User set genre:", self.user_genre

    def set_user_type(self, text):
        self.user_type = text
        print "User set type:", self.user_type

    def set_user_key(self, text):
        self.user_key = text
        print "User set key:", self.user_key

    def set_user_mode(self, text):
        self.user_mode = "+" if text == "Major" else "-"
        print "User set mode:", self.user_mode

    def set_user_tsig(self, text):
        self.user_tsig = text[:1]
        print "User set time signature:", self.user_tsig
