import time
import rtmidi
import threading
import watchman
import conductor
import tools
import chords
import melody
import bass
import lily
import recorder
import mixer
import profiles
import section

midiout = None
main_beat = 0

# ALL TO CHANGE
bar = 0
tempo_in_time = 0
bpm = 0
tsig = 0
timing = 0
buff = 0

tacet = ". . . . . . . . . . . . . . . ."
drumtacet = "H................ S................ K................"

drumlines = [drumtacet]
basslines = [tacet]
chordlines = [tacet]
melodylines = [tacet]

def write_things(parent):
    if parent.user_sheetmusic: lily.make(parent)
    if parent.user_midioutput: recorder.make(parent)

def init_features(parent):
    global timing, buff, bar

    timing = 4
    buff = 1
    bar = -buff
    update_features(parent)

def update_features(parent):
    global bpm, tempo_in_time, tsig

    bpm = int(parent.user_tempo)
    tempo_in_time = float(60.0 / float(bpm)) / float(parent.user_tempo_modifier)
    tsig = float(parent.user_tsig)

def kill_all():
    for i in xrange(len(mixer.channels)):
        chan = i + 144
        for note in xrange(0,127):
            midiout.send_message([chan, note, 0])

def kill_channel(chan):
    for note in xrange(0,127):
        midiout.send_message([chan, note, 0])

def kill_chord(chord):
    for note in chord: 
        midiout.send_message([mixer.get_channel("chords"), note, 0])

def play_note(chan, note, length):
    velo = mixer.get_volume(mixer.get_channelname(chan))
    threading.Thread(target = midiout.send_message, args = [[chan, note, velo]]).start()
    threading.Timer(tempo_in_time * length, midiout.send_message, [[chan, note, 0]]).start()

def play_notes(chan, chord, delay, length, chordsize):
    chord = chord[:chord[chordsize]]
    velo = mixer.get_volume("chords")
    for note in chord:
        threading.Thread(target = midiout.send_message, args = [[chan, note, velo]]).start()
        threading.Timer(tempo_in_time * length, midiout.send_message, [[chan, note, 0]]).start()

def play_chord(chan, speed, pattern):
    beat = 0
    while beat < (tsig * timing):        
        noteinfo = pattern[beat]
        
        if noteinfo != "." and noteinfo.startswith("r") == False:
            chord = tools.get_chord(noteinfo)
            length = tools.lengths[str(noteinfo[-2:])]
            chordsize = 6 * int(tools.invlerp(0, 100, profiles.motion))
            threading.Thread(target = play_notes, args = [chan,chord,0,length,chordsize]).start()

        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def play_bass(chan, speed, pattern):
    beat = 0
    while beat < (tsig * timing):
        noteinfo = pattern[beat]
        
        if noteinfo != "." and noteinfo.startswith("r") == False:
            if len(noteinfo) == 5:
                pitch = noteinfo[:2]
            else:
                pitch = noteinfo[:1]

            octave = int(noteinfo[-3:-2])
            length = tools.lengths[str(noteinfo[-2:])]
            conv_note = tools.roots[pitch] + (octave*12) + 24
            # play_note(midiout,chan,conv_note,length)
            threading.Thread(target = play_note, args = [chan,conv_note,length]).start()

        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def play_drums(chan, speed, pattern):
    beat = 0
    while beat < (tsig * timing):
        firelength = 0.02
        notestoplay = []

        # HATS
        if pattern[0][beat] == "x":
            notestoplay.append(42)

        # SNARE
        if pattern[1][beat] == "x":
            notestoplay.append(40)

        # KICK
        if pattern[2][beat] == "x":
            notestoplay.append(36)

        for note in notestoplay:
            threading.Thread(target = play_note, args = [chan, note, firelength]).start()

        del notestoplay
        
        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def play_melody(chan, speed, pattern):
    beat = 0
    while beat < (tsig * timing):
        noteinfo = pattern[beat]
        
        if noteinfo != "." and noteinfo.startswith("r") == False:
            if len(noteinfo) == 5:
                pitch = noteinfo[:2]
            else:
                pitch = noteinfo[:1]

            octave = int(noteinfo[-3:-2])
            length = tools.lengths[str(noteinfo[-2:])]
            conv_note = tools.roots[pitch] + (octave*12) + 24
            # play_note(midiout,chan,conv_note,length)
            threading.Thread(target = play_note, args = [chan,conv_note,length]).start()

        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def enqueue_drums(parent):
    if watchman.active == True:
        if len(drumlines) < buff: add_drums(drumtacet) 

        if len(drumlines) > 0:
            current_bar = drumlines[0].split()
            beatarray = [list(current_bar[0][1:]),list(current_bar[1][1:]),list(current_bar[2][1:])]
            play_drums(mixer.get_channel("drums"), tempo_in_time, beatarray)
            if parent.user_midioutput: recorder.add_drums_bar(beatarray)
            drumlines.pop(0)

def enqueue_bass(parent):
    if watchman.active == True:
        if len(basslines) < buff: add_bass(tacet)
        
        if len(basslines) > 0:
            thisone = basslines[0].split()
            play_bass(mixer.get_channel("bass"), tempo_in_time, list(thisone))
            if parent.user_sheetmusic: lily.add_bass_bar(thisone)
            if parent.user_midioutput: recorder.add_bass_bar(thisone)
            basslines.pop(0)

def enqueue_chords(parent):
    if watchman.active == True:
        if len(chordlines) < buff: add_chords(tacet)

        if len(chordlines) > 0:
            thisone = chordlines[0].split()
            play_chord(mixer.get_channel("chords"), tempo_in_time, list(thisone))
            if parent.user_sheetmusic: lily.add_chords_bar(thisone)
            if parent.user_midioutput: recorder.add_chords_bar(thisone)
            chordlines.pop(0)

def enqueue_melody(parent):
    if watchman.active == True:
        if len(melodylines) < buff: add_melody(tacet)

        if len(melodylines) > 0:
            thisone = melodylines[0].split()
            play_melody(mixer.get_channel("melody"), tempo_in_time, list(thisone))
            if parent.user_sheetmusic: lily.add_melody_bar(thisone)
            if parent.user_midioutput: recorder.add_melody_bar(thisone)
            melodylines.pop(0)

def enqueue(parent):
    while watchman.active == True:
        threading.Timer(0,enqueue_drums,[parent]).start()
        threading.Timer(0,enqueue_bass,[parent]).start()
        threading.Timer(0,enqueue_chords,[parent]).start()
        threading.Timer(0,enqueue_melody,[parent]).start()

        processing = 0.1
        time.sleep(float(tempo_in_time * timing) + processing)
        kill_all()

    kill_all()

def add_bass(pattern):
    basslines.append(pattern)

def add_drums(pattern):
    drumlines.append(pattern)

def add_chords(pattern):
    chordlines.append(pattern)

def add_melody(pattern):
    melodylines.append(pattern)

def monitor_beat(parent):
    while watchman.active == True:
        global main_beat
        main_beat += 1
        threading.Thread(target=play_note, args=(mixer.get_channel("metronome"), 37, tempo_in_time)).start()
        time.sleep(float(0.5))   

    write_things(parent)

def monitor_bar(parent):
    while watchman.active == True:
        update_features(parent)

        global bar

        print "Bar: \t", bar
        print "Key (rel.): \t", conductor.relativekey, conductor.relativemode
        print "Melo: \t", "(" + str(watchman.activities["melody"]) + ")\t", melodylines
        print "Chor: \t", "(" + str(watchman.activities["chords"]) + ")\t", chordlines 
        print "Bass: \t", "(" + str(watchman.activities["bass"]) + ")\t", basslines 
        print "Drum: \t", "(" + str(watchman.activities["drums"]) + ")\t", drumlines 
        print "Sect: \t", "(" + str(watchman.activities["section"]) + ")\t", section.rhythm
        print ""

        bar += 1

        bass.b_lock = False
        melody.m_lock = False
        chords.c_lock = False

        time.sleep(float(tempo_in_time) * float(tsig))

def start(parent):
    global midiout
    midiout = rtmidi.MidiOut(1)
    available_ports = midiout.get_ports()
    print "Available ports:",available_ports

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    init_features(parent)

    print "Playing..."

    threading.Thread(target = enqueue, args = [parent]).start()
    threading.Thread(target = monitor_bar, args = [parent]).start()
    threading.Thread(target = monitor_beat, args = [parent]).start()
