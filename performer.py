import time
import rtmidi
import threading
import watchman
import conductor
import general_composer
import chord_composer
import bass_composer
import lily
import recorder
import mixer

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
chords = [tacet]
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

def kill_all(midiout):
    for i in xrange(len(mixer.channels)):
        chan = i + 144
        for note in xrange(1,127):
            midiout.send_message([chan, note, 0])

def kill_channel(midiout, chan):
    for note in xrange(1,127):
        midiout.send_message([chan, note, 0])

def kill_chord(midiout, chord):
    for note in chord: 
        midiout.send_message([mixer.get_channel("chords"), note, 0])

def play_note(midiout, chan, note, length):
    velo = mixer.get_volume(mixer.get_channelname(chan))
    midiout.send_message([chan, note, velo])
    time.sleep(tempo_in_time * length)
    midiout.send_message([chan, note, 0])

def play_notes(midiout, chan, chord, delay, length, chordsize):
    chord = chord[:chord[chordsize]]
    velo = mixer.get_volume("chords")
    for note in chord:
        midiout.send_message([chan, note, velo])

    time.sleep(tempo_in_time * tsig)

    for note in chord:
        midiout.send_message([chan, note, 0])

def play_chord(midiout, chan, speed, beat, pattern):
    while beat < (tsig * timing):        
        noteinfo = pattern[beat]
        
        if noteinfo != ".":
            chord = general_composer.get_chord(noteinfo)
            length = noteinfo[-1:]
            chordsize = 6
            # play_notes(midiout,chan,chord,0,length,chordsize)
            threading.Timer(0,play_notes,[midiout,chan,chord,0,length,chordsize]).start()

        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def play_bass(midiout, chan, speed, beat, pattern):
    while beat < (tsig * timing):
        noteinfo = pattern[beat]
        
        if noteinfo != "." and noteinfo.startswith("r") == False:
            if len(noteinfo) == 5:
                pitch = noteinfo[:2]
            else:
                pitch = noteinfo[:1]

            octave = int(noteinfo[-3:-2])
            length = general_composer.lengths[str(noteinfo[-2:])]
            conv_note = general_composer.roots[pitch] + (octave*12) + 24
            # play_note(midiout,chan,conv_note,length)
            threading.Timer(0,play_note,[midiout,chan,conv_note,length]).start()

        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def play_drums(midiout, chan, speed, beat, pattern):
    while beat < (tsig * timing):
        # HATS
        if pattern[0][beat] == "x":
            play_note(midiout,chan,42,0.01)

        # SNARE
        if pattern[1][beat] == "x":
            play_note(midiout,chan,40,0.01)

        # KICK
        if pattern[2][beat] == "x":
            play_note(midiout,chan,36,0.01)
        
        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def play_melody(midiout, chan, speed, beat, pattern):
    while beat < (tsig * timing):
        noteinfo = pattern[beat]
        
        if noteinfo != "." and noteinfo.startswith("r") == False:
            if len(noteinfo) == 5:
                pitch = noteinfo[:2]
            else:
                pitch = noteinfo[:1]

            octave = int(noteinfo[-3:-2])
            length = general_composer.lengths[str(noteinfo[-2:])]
            conv_note = general_composer.roots[pitch] + (octave*12) + 24
            # play_note(midiout,chan,conv_note,length)
            threading.Timer(0,play_note,[midiout,chan,conv_note,length]).start()

        nextbeat = float(float(speed)/float(timing))
        time.sleep(nextbeat)
        beat += 1

def enqueue_drums(midiout, parent):
    if len(drumlines) < buff: add_drums(drumtacet) 

    current_bar = drumlines[0].split()
    beatarray = [list(current_bar[0][1:]),list(current_bar[1][1:]),list(current_bar[2][1:])]

    play_drums(midiout, mixer.get_channel("drums"), tempo_in_time, 0, beatarray)

    drumlines.pop(0)

def enqueue_bass(midiout, parent):
    if len(basslines) < buff: add_bass(tacet)

    play_bass(midiout, mixer.get_channel("bass"), tempo_in_time, 0, list(basslines[0].split()))
    
    if parent.user_sheetmusic: lily.add_bass_bar(basslines[0].split())
    if parent.user_midioutput: recorder.add_bass_bar(basslines[0].split())

    basslines.pop(0)

def enqueue_chords(midiout, parent):
    if len(chords) < buff: add_chords(tacet)

    play_chord(midiout, mixer.get_channel("chords"), tempo_in_time, 0, list(chords[0].split()))
    
    if parent.user_sheetmusic: lily.add_chords_bar(chords[0].split())
    if parent.user_midioutput: recorder.add_chords_bar(chords[0].split())
    
    chords.pop(0)

def enqueue_melody(midiout, parent):
    if len(melodylines) < buff: add_melody(tacet)

    play_melody(midiout, mixer.get_channel("melody"), tempo_in_time, 0, list(melodylines[0].split()))
    
    if parent.user_sheetmusic: lily.add_melody_bar(melodylines[0].split())
    if parent.user_midioutput: recorder.add_melody_bar(melodylines[0].split())

    melodylines.pop(0)

def enqueue(midiout, parent):
    while watchman.active == True:
        threading.Timer(0,enqueue_drums,[midiout, parent]).start()
        threading.Timer(0,enqueue_bass,[midiout, parent]).start()
        threading.Timer(0,enqueue_chords,[midiout, parent]).start()
        threading.Timer(0,enqueue_melody,[midiout, parent]).start()

        processing = 0.1
        time.sleep(float(tempo_in_time * timing) + processing)
        kill_all(midiout)

    kill_all(midiout)

def add_bass(pattern):
    basslines.append(pattern)

def add_drums(pattern):
    drumlines.append(pattern)

def add_chords(pattern):
    chords.append(pattern)

def add_melody(pattern):
    melodylines.append(pattern)

def monitor_beat(parent):
    while watchman.active == True:
        global main_beat
        main_beat += 1

        time.sleep(float(tempo_in_time))

    write_things(parent)

def monitor_bar(parent):
    while watchman.active == True:
        update_features(parent)

        global bar

        print "Bar: \t", bar
        print "Key: \t", conductor.relativekey, conductor.relativemode
        print "Melo: \t", melodylines
        print "Chor: \t", chords 
        print "Bass: \t", basslines 
        print "Drum: \t", drumlines 
        print ""

        bar += 1

        time.sleep(float(tempo_in_time) * float(tsig))

def start(midiout,parent):
    available_ports = midiout.get_ports()
    print "Available ports:",available_ports

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    init_features(parent)

    print "Playing..."

    threading.Timer(0,enqueue,[midiout,parent]).start()
    threading.Timer(0,monitor_bar,[parent]).start()
    threading.Timer(0,monitor_beat,[parent]).start()

    del midiout
