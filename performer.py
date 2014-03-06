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
    tempo_in_time = float(60.0 / float(bpm))
    tsig = float(parent.user_tsig)

def kill_all(midiout, chan):
    for note in xrange(1,100):
        midiout.send_message([chan, note, 0])

def kill_chord(midiout, chord):
    for note in chord: 
        midiout.send_message([mixer.get_channel("chords"), note, 0])

def play_note(midiout, chan, note, velo, length):
    midiout.send_message([chan, note, velo])
    time.sleep(tempo_in_time * length)
    midiout.send_message([chan, note, 0])

def play_notes(midiout, chan, chord, velo, delay, length, chordsize):
    chord = chord[:chord[chordsize]]
    for note in chord:
        midiout.send_message([chan, note, velo])

    time.sleep(tempo_in_time * tsig)

    # for note in chord:
        # midiout.send_message([chan, note, 0])

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
    
    if noteinfo != "." and noteinfo.startswith("r") == False:
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

def play_melody(midiout, chan, speed, vol, beat, loop, pattern):
    melodyarray = list(pattern)
    noteinfo = melodyarray[(beat % (int(tsig)*timing) - 1)]
    
    if noteinfo != "." and noteinfo.startswith("r") == False:
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
        threading.Timer(speed/timing,play_melody,[midiout, chan, speed, vol, beat, loop, pattern]).start()


def enqueue_drums(midiout, parent):
    while watchman.active == True:
        if len(drumlines) < buff: add_drums(drumtacet) 

        play_drums(midiout, mixer.get_channel("drums"), tempo_in_time, 127, 1, 0, drumlines[0].split())
        time.sleep(tempo_in_time*tsig)
        drumlines.pop(0)

    kill_all(midiout, mixer.get_channel("drums"))

def enqueue_bass(midiout, parent):
    while watchman.active == True:
        if len(basslines) < buff: add_bass(tacet)

        play_bass(midiout, mixer.get_channel("bass"), tempo_in_time, 127, 1, 0, basslines[0].split())
        
        if parent.user_sheetmusic: lily.add_bass_bar(basslines[0].split())
        if parent.user_midioutput: recorder.add_bass_bar(basslines[0].split())

        time.sleep(float(tempo_in_time*tsig))
        basslines.pop(0)

    kill_all(midiout, mixer.get_channel("bass"))

def enqueue_chords(midiout, parent):
    while watchman.active == True:
        if len(chords) < buff: add_chords(tacet)

        play_chord(midiout, mixer.get_channel("chords"), tempo_in_time, 127, 1, 0, chords[0].split())
        
        if parent.user_sheetmusic: lily.add_chords_bar(chords[0].split())
        if parent.user_midioutput: recorder.add_chords_bar(chords[0].split())
        
        time.sleep(float(tempo_in_time*tsig))
        chords.pop(0)

    kill_all(midiout, mixer.get_channel("chords"))

def enqueue_melody(midiout, parent):
    while watchman.active == True:
        if len(melodylines) < buff: add_melody(tacet)

        play_melody(midiout, mixer.get_channel("melody"), tempo_in_time, 127, 1, 0, melodylines[0].split())
        
        if parent.user_sheetmusic: lily.add_melody_bar(melodylines[0].split())
        if parent.user_midioutput: recorder.add_melody_bar(melodylines[0].split())

        time.sleep(float(tempo_in_time*tsig))
        melodylines.pop(0)

    kill_all(midiout, mixer.get_channel("melody"))

def add_bass(pattern):
    basslines.append(pattern)

def add_drums(pattern):
    drumlines.append(pattern)

def add_chords(pattern):
    chords.append(pattern)

def add_melody(pattern):
    melodylines.append(pattern)

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

def monitor_beat(parent):
    while watchman.active == True:
        global main_beat
        main_beat += 1

        time.sleep(tempo_in_time)

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
        # print "Drum", drumlines 
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
    threading.Timer(0,enqueue_melody,[midiout,parent]).start()
    threading.Timer(0,monitor_bar,[parent]).start()
    threading.Timer(0,monitor_beat,[parent]).start()

    del midiout

if __name__ == '__main__':
    test()

