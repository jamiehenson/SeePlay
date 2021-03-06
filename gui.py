from PySide import QtGui, QtCore
import pymouse
import watchman
import collections
import threading
import time
import mixer

window_w = 640 
window_h = 400

class SPApp(QtGui.QMainWindow):

    orch_text = "A light orchestral accompaniment, reacting to colour changes."
    elec_text = "A soft-pad synth accompaniment, reacting to colour changes."
    horr_text = "A highly reactive accompaniment, with orchestral instrumentation."
    sile_text = "A reactive solo piano accompaniment."
    acti_text = "A reactive and frantic orchestral accompaniment."

    infotexts = collections.OrderedDict()
    prog_types = collections.OrderedDict()
    mode_types = collections.OrderedDict()

    user_inputsrc = ""
    user_inputsrcinfo = ""
    user_type = ""
    user_genre = ""
    user_key = ""
    user_mode = ""
    user_tempo = ""
    user_tempo_modifier = ""
    user_tsig = ""
    user_inputregion = []
    user_score_title = "SeePlay auto-score"
    user_sheetmusic = False
    user_midioutput = False
    user_prog_type = ""

    screen_x = 0
    screen_y = 0

    def __init__(self):
        super(SPApp, self).__init__()
        self.init_ui()
        self.open_mixer()

    def populate_dictionaries(self):
        self.infotexts["Standard A"] = "A standard, balanced ambient profile. (colour driven)"
        # self.infotexts["Standard B"] = "A standard, balanced ambient profile. (motion driven)"
        # self.infotexts["Sparse"] = "A more spaced out ambient profile."

        self.prog_types["None"] = "none"
        self.prog_types["Random"] = "random"
        self.prog_types["Relative (I VI)"] = "relative"
        self.prog_types["Blues (I IV V)"] = "blues"
        self.prog_types["I to V"] = "fifth"
        self.prog_types["50s (I VI IV V)"] = "50s"
        self.prog_types["Circle of fifths"] = "circ5"
        self.prog_types["Circle of fourths"] = "circ4"

        self.mode_types["Major"] = "major"
        self.mode_types["Minor"] = "minor"
        self.mode_types["Ionian"] = "ionian"
        self.mode_types["Dorian"] = "dorian"
        self.mode_types["Phrygian"] = "phrygian"
        self.mode_types["Lydian"] = "lydian"
        self.mode_types["Mixolydian"] = "mixolydian"
        self.mode_types["Aeolian"] = "aeolian"
        self.mode_types["Locrian"] = "locrian"
        self.mode_types["Arabic"] = "arabic"

    def init_ui(self):
        self.center()
        self.setWindowTitle('SeePlay')
        self.setFixedSize(window_w, window_h)

        m = pymouse.PyMouse()
        screencoords = m.screen_size()
        self.screen_x = int(screencoords[0])
        self.screen_y = int(screencoords[1])

        boxheight = 30

        self.populate_dictionaries()

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
        midiout_slot = 3
        sheetout_slot = 4
        mixer_slot = 5

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
        stopbtn.resize(window_w * 0.33 - 10, boxheight * 1)
        stopbtn.move(5, ((stop_slot * boxheight) + title.height() + 5) - 5)
        stopbtn.clicked.connect(lambda: self.stop_watch())

        self.midibtn = QtGui.QCheckBox(self)
        self.midibtn.resize(window_w * 0.33 - 10, boxheight * 1)
        self.midibtn.move(10, ((midiout_slot * boxheight) + title.height() + 5) - 5)
        self.midibtn.setChecked(False)
        self.midibtn.stateChanged.connect(self.set_user_midioutput)

        self.midibtnlbl = QtGui.QLabel('Generate MIDI file?', self)
        self.midibtnlbl.resize(window_w * 0.33 - 10, boxheight * 1)
        self.midibtnlbl.move(25, ((midiout_slot * boxheight) + title.height() + 5) - 5)
        self.midibtnlbl.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")

        self.sheetbtn = QtGui.QCheckBox(self)
        self.sheetbtn.resize(window_w * 0.33 - 10, boxheight * 1)
        self.sheetbtn.move(10, ((sheetout_slot * boxheight) + title.height() + 5) - 5)
        self.sheetbtn.setChecked(False)
        self.sheetbtn.stateChanged.connect(self.set_user_sheetmusic)

        self.sheetbtnlbl = QtGui.QLabel('Generate sheet music?', self)
        self.sheetbtnlbl.resize(window_w * 0.33 - 10, boxheight * 1)
        self.sheetbtnlbl.move(25, ((sheetout_slot * boxheight) + title.height() + 5) - 5)
        self.sheetbtnlbl.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        mixerbtn = QtGui.QPushButton('OPEN MIXER', self)
        mixerbtn.resize(window_w * 0.33 - 10, boxheight * 1)
        mixerbtn.move(5, ((mixer_slot * boxheight) + title.height() + 5) - 5)
        mixerbtn.clicked.connect(lambda: self.open_mixer())

        # RIGHT BUTTONS
        # VISUAL SETTINGS

        # SLOTS
        visopt_slot = 0
        inputsrc_slot = 1
        inputsrcinfo_slot = 2
        audioopt_slot = 3
        type_slot = 4
        # genre_slot = 5
        genreinfo_slot = 5
        key_slot = 6
        mode_slot = 7
        prog_slot = 8
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
        self.inputsrcall.resize(window_w*0.25,boxheight)
        self.inputsrcall.move(window_w*0.33 + window_w*0.16, inputsrc_slot * boxheight + 5)
        self.inputsrcall.clicked.connect(lambda: self.set_user_inputsrc("whole", False))

        self.inputsrcreg = QtGui.QPushButton("Region",self)
        self.inputsrcreg.resize(window_w*0.25,boxheight)
        self.inputsrcreg.move(window_w*0.33 + window_w*0.41, inputsrc_slot * boxheight + 5)
        self.inputsrcreg.clicked.connect(lambda: self.set_user_inputsrc("manual", True))

        self.inputsrcinfo = QtGui.QLabel("",self)
        self.inputsrcinfo.resize(window_w*0.66,boxheight)
        self.inputsrcinfo.move(window_w * 0.33, inputsrcinfo_slot * boxheight + 5)
        self.inputsrcinfo.setStyleSheet("QLabel { padding: 5px; font-style: italic; font-size: 10px; text-align: center; color: #FFFFFF; }")
        
        # AUDIO SETTINGS
        stitle2 = QtGui.QLabel(self)
        stitle2.resize(window_w*0.68,boxheight)
        stitle2.move(window_w*0.33, (audioopt_slot * boxheight) + 10)
        stitle2.setText('Audio options')
        stitle2.setStyleSheet("QLabel { padding: 5px; font-size: 18px; text-align: center; background-color: rgba(200, 200, 200, 150); color: #333333; }")
        
        # Genre
        # genre = QtGui.QLabel(self)
        # genre.resize(window_w*0.16,boxheight)
        # genre.move(window_w*0.33, (genre_slot * boxheight) + 15)
        # genre.setText('Profile: ')
        # genre.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        # self.genrebox = QtGui.QComboBox(self)
        # self.genrebox.resize(window_w*0.5,boxheight)
        # self.genrebox.move(window_w*0.33 + window_w*0.16, (genre_slot * boxheight) + 15)
        # self.genrebox.addItem("Classical")
        # self.genrebox.addItem("Electronic")

        # Music type
        mustype = QtGui.QLabel(self)
        mustype.resize(window_w*0.16,boxheight)
        mustype.move(window_w*0.33, (type_slot * boxheight) + 15)
        mustype.setText('Profile: ')
        mustype.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.mustypebox = QtGui.QComboBox(self)
        self.mustypebox.resize(window_w*0.5,boxheight)
        self.mustypebox.move(window_w*0.33 + window_w*0.16, (type_slot * boxheight) + 15)
        sorted_profile = collections.OrderedDict(self.infotexts)
        for key, value in sorted_profile.iteritems():
            self.mustypebox.addItem(key)
        self.mustypebox.activated[str].connect(lambda: self.switch_genre_box(self.mustypebox.currentText()))
        # self.genrebox.activated[str].connect(lambda: self.switch_genre_info_box(self.genrebox.currentText()))

        # Genre Info
        self.genreinfo = QtGui.QLabel(self)
        self.genreinfo.resize(window_w*0.68,boxheight)
        self.genreinfo.setText(self.infotexts[self.mustypebox.currentText()])
        self.genreinfo.move(window_w*0.33, (genreinfo_slot * boxheight) + 15)
        self.genreinfo.setStyleSheet("QLabel { padding: 5px; font-size: 12px; font-weight: bold; text-align: center; color: #FFFFFF; }")

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
        mode.setText('Mode: ')
        mode.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.modebox = QtGui.QComboBox(self)
        self.modebox.resize(window_w*0.5,boxheight)
        self.modebox.move(window_w*0.33 + window_w*0.16, (mode_slot * boxheight) + 15)
        sorted_modes = collections.OrderedDict(self.mode_types)
        for key, value in sorted_modes.iteritems():
            self.modebox.addItem(key)
        self.modebox.activated[str].connect(lambda: self.set_user_mode(self.modebox.currentText()))

        # Key
        prog = QtGui.QLabel(self)
        prog.resize(window_w*0.16,boxheight)
        prog.move(window_w*0.33, (prog_slot * boxheight) + 15)
        prog.setText('Progression: ')
        prog.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.progbox = QtGui.QComboBox(self)
        self.progbox.resize(window_w*0.5,boxheight)
        self.progbox.move(window_w*0.33 + window_w*0.16, (prog_slot * boxheight) + 15)
        sorted_prog = collections.OrderedDict(self.prog_types)
        for key, value in sorted_prog.iteritems():
            self.progbox.addItem(key)
        self.progbox.activated[str].connect(lambda: self.set_user_prog_type(self.progbox.currentText()))

        # Time sig
        sig = QtGui.QLabel(self)
        sig.resize(window_w*0.16,boxheight)
        sig.move(window_w*0.33, (tsig_slot * boxheight) + 15)
        sig.setText('Time signature: ')
        sig.setStyleSheet("QLabel { padding: 5px; font-size: 12px; text-align: center; color: #FFFFFF; }")
        
        self.sigbox = QtGui.QComboBox(self)
        self.sigbox.resize(window_w*0.5,boxheight)
        self.sigbox.move(window_w*0.33 + window_w*0.16, (tsig_slot * boxheight) + 15)
        # self.sigbox.addItem("3/4")
        self.sigbox.addItem("4/4")
        # self.sigbox.addItem("5/4")
        self.sigbox.setCurrentIndex(0)
        self.sigbox.activated[str].connect(lambda: self.set_user_tsig(self.sigbox.currentText()))
        
        # Tempo
        self.tempo = QtGui.QLabel(self)
        self.tempo.resize(window_w*0.16,boxheight)
        self.tempo.move(window_w*0.33, (tempo_slot * boxheight) + 15)
        self.tempo.setText('Tempo: ')
        self.tempo.setStyleSheet("QLabel { padding: 5px; font-size: 8px; text-align: center; color: #FFFFFF; }")
        
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

    def open_mixer(self):
        print "Opening mixer."

        mix_w = 400
        row_w = mix_w / 4
        row_h = 30
        mix_h = row_h * 10

        firstcolx = 0
        secondcolx = row_w
        thirdcolx = row_w * 2

        title_slot = 0
        stitle_slot = 1
        header_slot = 2
        drums_slot = 3
        bass_slot = 4
        chords_slot = 5
        melody_slot = 6
        stabs_slot = 7
        metro_slot = 8
        info_slot = 9

        self.mix = QtGui.QWidget()

        self.mix.resize(mix_w, mix_h)
        self.mix.setWindowTitle('SeePlay Mixer')
        self.center()

        mixbg = QtGui.QLabel(self.mix)
        mixbg.resize(mix_w, mix_h)
        mixbg.move(0, 0)
        mixbg.setStyleSheet("QLabel { background-color: #333333; color: #EEEEEE; }")

        mixtitle = QtGui.QLabel(self.mix)
        mixtitle.resize(mix_w, row_h)
        mixtitle.move(0, row_h * title_slot)
        mixtitle.setText('SeePlay Mixer')
        mixtitle.setStyleSheet("QLabel { padding: 5px; font-size: 18px; text-align: center; background-color: rgba(100, 100, 100, 100); color: #FFFFFF; }")

        mixstitle = QtGui.QLabel(self.mix)
        mixstitle.resize(mix_w, row_h)
        mixstitle.move(0, row_h * stitle_slot)
        mixstitle.setText('Assign the instrument channels for MIDI output (0-15).')
        mixstitle.setStyleSheet("QLabel { padding: 5px; font-size: 10px; text-align: center; background-color: rgba(200, 200, 200, 150); color: #333333; }")

        self.mix.inst = QtGui.QLabel("Instrument:", self.mix)
        self.mix.inst.resize(row_w, row_h)
        self.mix.inst.move(firstcolx, row_h * header_slot)
        self.mix.inst.setStyleSheet("QLabel { padding: 5px; font-size: 16px; text-align: center; color: #FFFFFF; }")

        self.mix.chan = QtGui.QLabel("Channel:", self.mix)
        self.mix.chan.resize(row_w, row_h)
        self.mix.chan.move(secondcolx, row_h * header_slot)
        self.mix.chan.setStyleSheet("QLabel { padding: 5px; font-size: 16px; text-align: center; color: #FFFFFF; }")

        self.mix.vol = QtGui.QLabel("Volume (auto):", self.mix)
        self.mix.vol.resize(row_w * 2, row_h)
        self.mix.vol.move(thirdcolx, row_h * header_slot)
        self.mix.vol.setStyleSheet("QLabel { padding: 5px; font-size: 16px; text-align: center; color: #FFFFFF; }")

        self.mix.drums = QtGui.QLabel("Drums:", self.mix)
        self.mix.drums.resize(row_w, row_h)
        self.mix.drums.move(firstcolx, row_h * drums_slot)
        self.mix.drums.setStyleSheet("QLabel { padding: 5px; font-size: 14px; font-weight: bold; text-align: center; color: #FFFFFF; }")

        self.mix.drumbox = QtGui.QComboBox(self.mix)
        self.mix.drumbox.resize(row_w, row_h)
        self.mix.drumbox.move(secondcolx,row_h * drums_slot)
        for i in xrange(16):
            self.mix.drumbox.addItem(str(i))
        self.mix.drumbox.addItem("Off")
        self.mix.drumbox.setCurrentIndex(mixer.get_stdchannel("drums"))
        self.mix.drumbox.activated[str].connect(lambda: mixer.set_channel("drums", self.mix.drumbox.currentText()))

        self.mix.drumvol = QtGui.QSlider(QtCore.Qt.Horizontal, self.mix)
        self.mix.drumvol.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mix.drumvol.resize(row_w * 2, row_h)
        self.mix.drumvol.move(thirdcolx, row_h * drums_slot)
        self.mix.drumvol.setMinimum(0)
        self.mix.drumvol.setMaximum(127)
        self.mix.drumvol.setValue(mixer.get_volume("drums"))
        self.mix.drumvol.valueChanged[int].connect(lambda: mixer.set_volume(self, "drums", self.mix.drumvol.value()))

        self.mix.bass = QtGui.QLabel("Bass:", self.mix)
        self.mix.bass.resize(secondcolx, row_h)
        self.mix.bass.move(firstcolx, row_h * bass_slot)
        self.mix.bass.setStyleSheet("QLabel { padding: 5px; font-size: 14px; font-weight: bold; text-align: center; color: #FFFFFF; }")

        self.mix.bassbox = QtGui.QComboBox(self.mix)
        self.mix.bassbox.resize(row_w, row_h)
        self.mix.bassbox.move(secondcolx,row_h * bass_slot)
        for i in xrange(16):
            self.mix.bassbox.addItem(str(i))
        self.mix.bassbox.addItem("Off")
        self.mix.bassbox.setCurrentIndex(mixer.get_stdchannel("bass"))
        self.mix.bassbox.activated[str].connect(lambda: mixer.set_channel("bass", self.mix.bassbox.currentText()))

        self.mix.bassvol = QtGui.QSlider(QtCore.Qt.Horizontal, self.mix)
        self.mix.bassvol.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mix.bassvol.resize(row_w * 2, row_h)
        self.mix.bassvol.move(thirdcolx, row_h * bass_slot)
        self.mix.bassvol.setMinimum(0)
        self.mix.bassvol.setMaximum(127)
        self.mix.bassvol.setValue(mixer.get_volume("bass"))
        self.mix.bassvol.valueChanged[int].connect(lambda: mixer.set_volume(self, "bass", self.mix.bassvol.value()))

        self.mix.chords = QtGui.QLabel("Chords:", self.mix)
        self.mix.chords.resize(row_w, row_h)
        self.mix.chords.move(firstcolx, row_h * chords_slot)
        self.mix.chords.setStyleSheet("QLabel { padding: 5px; font-size: 14px; font-weight: bold; text-align: center; color: #FFFFFF; }")

        self.mix.chordsbox = QtGui.QComboBox(self.mix)
        self.mix.chordsbox.resize(row_w, row_h)
        self.mix.chordsbox.move(secondcolx,row_h * chords_slot)
        for i in xrange(16):
            self.mix.chordsbox.addItem(str(i))
        self.mix.chordsbox.addItem("Off")
        self.mix.chordsbox.setCurrentIndex(mixer.get_stdchannel("chords"))
        self.mix.chordsbox.activated[str].connect(lambda: mixer.set_channel("chords", self.mix.chordsbox.currentText()))

        self.mix.chordsvol = QtGui.QSlider(QtCore.Qt.Horizontal, self.mix)
        self.mix.chordsvol.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mix.chordsvol.resize(row_w * 2, row_h)
        self.mix.chordsvol.move(thirdcolx, row_h * chords_slot)
        self.mix.chordsvol.setMinimum(0)
        self.mix.chordsvol.setMaximum(127)
        self.mix.chordsvol.setValue(100)
        self.mix.chordsvol.valueChanged[int].connect(lambda: mixer.set_volume(self, "chords", self.mix.chordsvol.value()))

        self.mix.melody = QtGui.QLabel("Melody:", self.mix)
        self.mix.melody.resize(row_w, row_h)
        self.mix.melody.move(firstcolx, row_h * melody_slot)
        self.mix.melody.setStyleSheet("QLabel { padding: 5px; font-size: 14px; font-weight: bold; text-align: center; color: #FFFFFF; }")

        self.mix.melodybox = QtGui.QComboBox(self.mix)
        self.mix.melodybox.resize(row_w, row_h)
        self.mix.melodybox.move(secondcolx,row_h * melody_slot)
        for i in xrange(16):
            self.mix.melodybox.addItem(str(i))
        self.mix.melodybox.addItem("Off")
        self.mix.melodybox.setCurrentIndex(mixer.get_stdchannel("melody"))
        self.mix.melodybox.activated[str].connect(lambda: mixer.set_channel("melody", self.mix.melodybox.currentText()))

        self.mix.melodyvol = QtGui.QSlider(QtCore.Qt.Horizontal, self.mix)
        self.mix.melodyvol.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mix.melodyvol.resize(row_w * 2, row_h)
        self.mix.melodyvol.move(thirdcolx, row_h * melody_slot)
        self.mix.melodyvol.setMinimum(0)
        self.mix.melodyvol.setMaximum(127)
        self.mix.melodyvol.setValue(100)
        self.mix.melodyvol.valueChanged[int].connect(lambda: mixer.set_volume(self, "melody", self.mix.melodyvol.value()))

        self.mix.stabs = QtGui.QLabel("Stabs:", self.mix)
        self.mix.stabs.resize(row_w, row_h)
        self.mix.stabs.move(firstcolx, row_h * stabs_slot)
        self.mix.stabs.setStyleSheet("QLabel { padding: 5px; font-size: 14px; font-weight: bold; text-align: center; color: #FFFFFF; }")

        self.mix.stabsbox = QtGui.QComboBox(self.mix)
        self.mix.stabsbox.resize(row_w, row_h)
        self.mix.stabsbox.move(secondcolx,row_h * stabs_slot)
        for i in xrange(16):
            self.mix.stabsbox.addItem(str(i))
        self.mix.stabsbox.addItem("Off")
        self.mix.stabsbox.setCurrentIndex(mixer.get_stdchannel("stabs"))
        self.mix.stabsbox.activated[str].connect(lambda: mixer.set_channel("stabs", self.mix.stabsbox.currentText()))

        self.mix.stabsvol = QtGui.QSlider(QtCore.Qt.Horizontal, self.mix)
        self.mix.stabsvol.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mix.stabsvol.resize(row_w * 2, row_h)
        self.mix.stabsvol.move(thirdcolx, row_h * stabs_slot)
        self.mix.stabsvol.setMinimum(0)
        self.mix.stabsvol.setMaximum(127)
        self.mix.stabsvol.setValue(100)
        self.mix.stabsvol.valueChanged[int].connect(lambda: mixer.set_volume(self, "stabs", self.mix.stabsvol.value()))

        self.mix.metro = QtGui.QLabel("Metronome:", self.mix)
        self.mix.metro.resize(row_w, row_h)
        self.mix.metro.move(firstcolx, row_h * metro_slot)
        self.mix.metro.setStyleSheet("QLabel { padding: 5px; font-size: 14px; font-weight: bold; text-align: center; color: #FFFFFF; }")

        self.mix.metrobox = QtGui.QComboBox(self.mix)
        self.mix.metrobox.resize(row_w, row_h)
        self.mix.metrobox.move(secondcolx,row_h * metro_slot)
        for i in xrange(16):
            self.mix.metrobox.addItem(str(i))
        self.mix.metrobox.addItem("Off")
        self.mix.metrobox.setCurrentIndex(mixer.get_stdchannel("metronome"))
        self.mix.metrobox.activated[str].connect(lambda: mixer.set_channel("metronome", self.mix.metrobox.currentText()))

        self.mix.metrovol = QtGui.QSlider(QtCore.Qt.Horizontal, self.mix)
        self.mix.metrovol.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mix.metrovol.resize(row_w * 2, row_h)
        self.mix.metrovol.move(thirdcolx, row_h * metro_slot)
        self.mix.metrovol.setMinimum(0)
        self.mix.metrovol.setMaximum(127)
        self.mix.metrovol.setValue(100)
        self.mix.metrovol.valueChanged[int].connect(lambda: mixer.set_volume(self, "metronome", self.mix.metrovol.value()))

        self.mix.info = QtGui.QLabel("Please use your connected DAW to control master volume.", self.mix)
        self.mix.info.resize(mix_w, row_h)
        self.mix.info.move(firstcolx, row_h * info_slot)
        self.mix.info.setStyleSheet("QLabel { padding: 5px; font-style: italic; font-size: 10px; text-align: center; color: #FFFFFF; }")

        self.mix.show()
        
    def switch_genre_box(self, text):
        self.set_user_type(text)
        self.genreinfo.setText(self.infotexts[text])

        # if text == "Ambient":
        #     self.genrebox.clear()
        #     self.genrebox.addItem("Classical")
        #     self.genrebox.addItem("Electronic")
        #     self.genreinfo.setText(self.orch_text)
        #     self.set_user_genre("Classical")
        # else:
        #     self.genrebox.clear()
        #     self.genrebox.addItem("Horror")
        #     self.genrebox.addItem("Silent Movie")
        #     self.genrebox.addItem("Action")
        #     self.genreinfo.setText(self.horr_text)
        #     self.set_user_genre("Horror")

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
            if self.sheetbtn.isChecked() or self.midibtn.isChecked():
                self.user_score_title, ok = QtGui.QInputDialog.getText(self, 'Name your piece!', 
                'Enter a title for your music:')

            watchman.active = True
            watchman.start_watching(self)

    def stop_watch(self):
        watchman.active = False
        print "Stopping."

    def set_initial_vars(self):
        print "----------------------------"
        self.set_user_inputsrc("whole",False)
        self.set_user_type(self.mustypebox.currentText())
        # self.set_user_genre(self.genrebox.currentText())
        self.set_user_key(self.keysigbox.currentText())
        self.set_user_mode(self.modebox.currentText())
        self.set_user_prog_type(self.progbox.currentText())
        self.set_user_tempo(self.tempobox.value())
        self.set_user_tempo_modifier("1.0")
        self.set_user_tsig(self.sigbox.currentText())
        print "----------------------------"

    def grab_region_point(self, count, first):
        mouse_pos = None

        if count > 0:
            m = pymouse.PyMouse()
            if first:
                txt = "Move your mouse to the top left corner of your region. (" + str(count) + " seconds remaining)"
            else:
                txt = "Move your mouse to the lower right corner of your region. (" + str(count) + " seconds remaining)"
            
            print txt
            self.inputsrcinfo.setText(txt)

            time.sleep(1)
            count -= 1
            mouse_pos = m.position()

            self.grab_region_point(count, first)
        else:
            if first:
                txt = "Top left coordinate saved. Moving to bottom right coordinate..."
            else:
                txt = "Bottom right coordinate saved."

            print txt
            self.inputsrcinfo.setText(txt)

            time.sleep(1)

        return mouse_pos

    def grab_region(self):
        topleft = self.grab_region_point(3, True)
        print topleft
        bottomright = self.grab_region_point(3, False)
        print bottomright

        x = topleft[0]
        y = topleft[1]
        w = abs(topleft[0] - bottomright[0])
        h = abs(topleft[1] - bottomright[1])

        self.user_inputregion = [int(x), int(y), int(w), int(h)]
        print self.user_inputregion
        self.inputsrcinfo.setText("Thanks! Selected region: (" + str(self.user_inputregion) + ")")

    def set_user_inputsrc(self, text, region):
        self.user_inputsrc = text
        self.set_user_inputsrcinfo(text)

        if region:
            threading.Timer(0, self.grab_region, []).start()

        #print "User set input source:", user_inputsrc

    def set_user_inputsrcinfo(self, text):
        if text == "whole":
            chosenText = "Capturing the whole screen."
        elif text == "active":
            chosenText = "Capturing the active window."
        elif text == "manual":
            chosenText = "Capturing a user-defined region."

        self.user_inputsrcinfo = chosenText
        self.inputsrcinfo.setText(self.user_inputsrcinfo)

        print "Use set input source:", self.user_inputsrcinfo

    def set_user_tempo(self, val):
        self.user_tempo = int(val)
        self.tempo.setText("Tempo: " + str(self.user_tempo) + " (x" + str(self.user_tempo_modifier) + ")")
        print "User set tempo:", self.user_tempo, self.user_tempo_modifier

    def set_user_tempo_modifier(self, val):
        self.user_tempo_modifier = float(val)
        self.tempo.setText("Tempo: " + str(self.user_tempo) + " (x" + str(self.user_tempo_modifier) + ")")
        print "User set tempo:", self.user_tempo, " x",self.user_tempo_modifier

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
        self.user_mode = self.mode_types[text]
        print "User set mode:", self.user_mode

    def set_user_prog_type(self, text):
        self.user_prog_type = self.prog_types[text]
        print "User set chord progression:", self.user_prog_type

    def set_user_tsig(self, text):
        self.user_tsig = text[:1]
        print "User set time signature:", self.user_tsig

    def set_user_sheetmusic(self):
        status = self.sheetbtn.isChecked()
        self.user_sheetmusic = status
        print "User requests sheet music:", self.user_sheetmusic

    def set_user_midioutput(self):
        status = self.midibtn.isChecked()
        self.user_midioutput = status
        print "User requests sheet music:", self.user_midioutput

    def set_volumebar(self, chan, val):
        if chan == "drums":
            self.mix.drumvol.setValue(val)
        if chan == "bass":
            self.mix.bassvol.setValue(val)
        if chan == "chords":
            self.mix.chordsvol.setValue(val)
        if chan == "melody":
            self.mix.melodyvol.setValue(val)