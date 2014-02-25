import time
import rtmidi
import threading
import watchman
import chordbuilder

beat = 1
bpm = 120
tsig = 4
timing = 4

drums_channel = 0x90
bass_channel = 0x91
chords_channel = 0x92

drumlines = ["H................ S................ K................"]
basslines = [". . . . . . . . . . . . . . . ."]
chords = [". . . . . . . . . . . . . . . ."]

def kill_all(midiout, chan):
    for note in xrange(1,100):
        note_off = [chan, note, 0]
        midiout.send_message(note_off)

def kill_chord(midiout, chord):
    for note in chord:
        note_off = [chords_channel, note, 0]
        midiout.send_message(note_off)

def play_note(midiout, chan, note, velo):
    note_on = [chan, note, velo]
    note_off = [0x80, note, 0]
    print note
    midiout.send_message(note_on)
    midiout.send_message(note_off)

def play_notes(midiout, chan, chord, velo, delay, length, chordsize):
    chord = chord[:chord[chordsize]]
    for note in chord:
        note_on = [chan, note, velo]
        midiout.send_message(note_on)
        time.sleep(delay)

    pause = 0.5 if length == "l" else 0
    # time.sleep(pause)

def play_chord(midiout, chan, speed, vol, beat, loop, pattern):
    chordarray = list(pattern)
    noteinfo = chordarray[(beat % (tsig*timing) - 1)]
    
    if noteinfo != ".":
        chord = chordbuilder.get_chord(noteinfo)
        length = noteinfo[-1:]
        play_notes(midiout,chan,chord,vol,0,length,chordsize)

    beat += 1
    loop += 1
    
    if loop < (tsig * 4):
        threading.Timer(speed/timing,play_bass,[midiout, chan, speed, vol, beat, loop, pattern]).start()

def play_bass(midiout, chan, speed, vol, beat, loop, pattern):
    bassarray = list(pattern)
    noteinfo = bassarray[(beat % (tsig*timing) - 1)]
    
    if noteinfo != ".":
        if len(noteinfo) == 3:
            pitch = noteinfo[:2]
        else:
            pitch = noteinfo[:1]

        octave = int(noteinfo[-1:])

        notes = {
           "C" : 24,
           "Db" : 25,
           "D" : 26,
           "Eb" : 27,
           "E" : 28,
           "F" : 29,
           "Gb" : 30,
           "G" : 31,
           "Ab" : 32,
           "A" : 33,
           "Bb" : 34,
           "B" : 35,
        }
    
        conv_note = notes[pitch] + (octave*12)
        play_note(midiout,chan,conv_note,vol)

    beat += 1
    loop += 1
    
    if loop < (tsig * 4):
        threading.Timer(speed/timing,play_bass,[midiout, chan, speed, vol, beat, loop, pattern]).start()

def play_drums(midiout, chan, speed, vol, beat, loop, pattern):
    beatarray = [list(pattern[0][1:]),list(pattern[1][1:]),list(pattern[2][1:])]

    # HATS
    if beatarray[0][(beat % (tsig*timing)) - 1] == "x":
        play_note(midiout,chan,42,vol)

    # SNARE
    if beatarray[1][(beat % (tsig*timing)) - 1] == "x":
        play_note(midiout,chan,40,vol)

    # KICK
    if beatarray[2][(beat % (tsig*timing)) - 1] == "x":
        play_note(midiout,chan,36,vol)

    beat += 1
    loop += 1

    if loop < (tsig * 4):
        threading.Timer(speed/timing, play_drums, [midiout, chan, speed, vol, beat, loop, pattern]).start()

def enqueue_drums(midiout, tempo):
    while watchman.active == True:
        play_drums(midiout, drums_channel, tempo, 100, beat, 0, drumlines[0].split())
        time.sleep(tempo*tsig)
        drumlines.pop(0)

    kill_all(midiout, drums_channel)

def enqueue_bass(midiout, tempo):
    while watchman.active == True:
        play_bass(midiout, bass_channel, tempo, 127, beat, 0, basslines[0].split())
        time.sleep(tempo*tsig)
        basslines.pop(0)

    kill_all(midiout, bass_channel)

def enqueue_chords(midiout, tempo):
    while watchman.active == True:
        play_chord(midiout, chords_channel, tempo, 127, beat, 0, chords[0].split())
        time.sleep(tempo*tsig)
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

    tempo_in_time = float(60.0/float(bpm))

    print "Tempo:",bpm
    print "Time signature:",tsig,"/ 4"
    print "Playing..."

    threading.Timer(0,enqueue_bass,[midiout,tempo_in_time]).start()
    threading.Timer(0,enqueue_drums,[midiout,tempo_in_time]).start()

    newpat = "C1 . . D1 . . E1 . . . F1 . G1 . . ."
    threading.Timer(1,add_bass,[newpat]).start()
    threading.Timer(1,add_bass,[newpat]).start()

    del midiout

def start(midiout):
    available_ports = midiout.get_ports()
    print "Available ports:",available_ports

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    tempo_in_time = float(60.0/float(bpm))

    print "Tempo:",bpm
    print "Time signature:",tsig,"/ 4"
    print "Playing..."

    threading.Timer(0,enqueue_bass,[midiout,tempo_in_time]).start()
    threading.Timer(0,enqueue_drums,[midiout,tempo_in_time]).start()
    threading.Timer(0,enqueue_chords,[midiout,tempo_in_time]).start()

    del midiout

if __name__ == '__main__':
    test()

