import time
import rtmidi
import threading
import watchman
import conductor
import general_composer
import chord_composer
import bass_composer


beat = 1

drums_channel = 0x90
bass_channel = 0x91
chords_channel = 0x92

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

def init_features(parent):
    global timing, buff, bar

    timing = 4
    buff = 2
    bar = -buff
    update_features(parent)

def update_features(parent):
    global bpm, tempo_in_time, tsig
    
    bpm = int(parent.user_tempo)
    tempo_in_time = float(60.0 / float(bpm))
    tsig = float(parent.user_tsig)

def kill_all(midiout, chan):
    for note in xrange(1,100):
        midiout.send_message([chan, note, 0])

def kill_chord(midiout, chord):
    for note in chord: 
        midiout.send_message([chords_channel, note, 0])

def play_note(midiout, chan, note, velo, length):
    midiout.send_message([chan, note, velo])
    time.sleep(tempo_in_time * length)
    midiout.send_message([chan, note, 0])

def play_notes(midiout, chan, chord, velo, delay, length, chordsize):
    chord = chord[:chord[chordsize]]
    for note in chord:
        midiout.send_message([chan, note, velo])

    time.sleep(tempo_in_time * tsig)

    for note in chord:
        midiout.send_message([chan, note, 0])

def play_chord(midiout, chan, speed, vol, beat, loop, pattern):
    chordarray = list(pattern)
    noteinfo = chordarray[(beat % (int(tsig)*timing) - 1)]
    
    if noteinfo != ".":
        chord = general_composer.get_chord(noteinfo)
        length = noteinfo[-1:]
        chordsize = 6
        threading.Timer(0,play_notes,[midiout,chan,chord,vol,0,length,chordsize]).start()

    beat += 1
    loop += 1
    
    if loop < (tsig * 4):
        threading.Timer(speed/timing,play_chord,[midiout, chan, speed, vol, beat, loop, pattern]).start()

def play_bass(midiout, chan, speed, vol, beat, loop, pattern):
    bassarray = list(pattern)
    noteinfo = bassarray[(beat % (int(tsig)*timing) - 1)]
    
    if noteinfo != ".":
        if len(noteinfo) == 5:
            pitch = noteinfo[:2]
        else:
            pitch = noteinfo[:1]

        octave = int(noteinfo[-3:-2])
        length = general_composer.lengths[str(noteinfo[-2:])]
        conv_note = general_composer.roots[pitch] + (octave*12) + 24
        threading.Timer(0,play_note,[midiout,chan,conv_note,vol,length]).start()

    beat += 1
    loop += 1
    
    if loop < (tsig * 4):
        threading.Timer(speed/timing,play_bass,[midiout, chan, speed, vol, beat, loop, pattern]).start()

def play_drums(midiout, chan, speed, vol, beat, loop, pattern):
    beatarray = [list(pattern[0][1:]),list(pattern[1][1:]),list(pattern[2][1:])]

    # HATS
    if beatarray[0][(beat % (int(tsig)*timing)) - 1] == "x":
        play_note(midiout,chan,42,vol)

    # SNARE
    if beatarray[1][(beat % (int(tsig)*timing)) - 1] == "x":
        play_note(midiout,chan,40,vol)

    # KICK
    if beatarray[2][(beat % (int(tsig)*timing)) - 1] == "x":
        play_note(midiout,chan,36,vol)

    beat += 1
    loop += 1

    if loop < (tsig * 4):
        threading.Timer(speed/timing, play_drums, [midiout, chan, speed, vol, beat, loop, pattern]).start()

def enqueue_drums(midiout, parent):
    while watchman.active == True:
        update_features(parent)

        if len(drumlines) < 2: add_drums(drumtacet) 

        play_drums(midiout, drums_channel, tempo_in_time, 127, beat, 0, drumlines[0].split())
        time.sleep(tempo_in_time*tsig)
        drumlines.pop(0)

    kill_all(midiout, drums_channel)

def enqueue_bass(midiout, parent):
    while watchman.active == True:
        update_features(parent)

        if len(basslines) < 2: add_bass(tacet)

        play_bass(midiout, bass_channel, tempo_in_time, 127, beat, 0, basslines[0].split())
        time.sleep(float(tempo_in_time*tsig))
        basslines.pop(0)

    kill_all(midiout, bass_channel)

def enqueue_chords(midiout, parent):
    while watchman.active == True:
        update_features(parent)

        if len(chords) < 2: add_chords(tacet)

        play_chord(midiout, chords_channel, tempo_in_time, 127, beat, 0, chords[0].split())
        time.sleep(float(tempo_in_time*tsig))
        chords.pop(0)

    kill_all(midiout, chords_channel)

def add_bass(pattern):
    basslines.append(pattern)

def add_drums(pattern):
    drumlines.append(pattern)

def add_chords(pattern):
    chords.append(pattern)

def test():
    midiout = rtmidi.MidiOut(1)
    available_ports = midiout.get_ports()
    print "Available ports:",available_ports

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    print "Tempo:",bpm
    print "Time signature:",tsig,"/ 4"
    print "Playing..."

    newpat = "C1 . . D1 . . E1 . . . F1 . G1 . . ."
    threading.Timer(1,add_bass,[newpat]).start()
    threading.Timer(1,add_bass,[newpat]).start()

    del midiout

def monitor():
    while watchman.active == True:
        global bar

        print "Bar: ", bar
        print "Key: ", conductor.relativekey, conductor.relativemode
        print "Chords", chords 
        print "Bass", basslines 
        # print "Drums", drumlines 
        print ""
        
        bar += 1

        time.sleep(tempo_in_time * tsig)

def start(midiout,parent):
    available_ports = midiout.get_ports()
    print "Available ports:",available_ports

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    init_features(parent)

    print "Playing..."

    threading.Timer(0,enqueue_bass,[midiout,parent]).start()
    threading.Timer(0,enqueue_drums,[midiout,parent]).start()
    threading.Timer(0,enqueue_chords,[midiout,parent]).start()
    threading.Timer(0,monitor).start()

    del midiout

if __name__ == '__main__':
    test()

