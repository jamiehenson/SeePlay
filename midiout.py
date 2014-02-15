import time
import rtmidi
import threading

beat = 1
bpm = 120
tsig = 4
timing = 4

drumlines = ["Hxxxxxxxxxxxxxxxx S.x..x....x..x... Kx.xx..xx..xx....", 
             "Hxxxxxxxxxxxxxxxx S.x.xx....x..x... Kx.xx..xx..xx...."]

basslines = ["C1 . . C1 . . Bb0 . . . Ab0 . G0 . . .",
             "C1 . . D1 . . Bb0 . . . Ab0 . G0 . . ."]

def playnote(midiout, chan, note, velo):
    note_on = [chan, note, velo] # channel 1, middle C, velocity 112
    note_off = [0x80, note, 0]
    midiout.send_message(note_on)
    midiout.send_message(note_off)

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
        playnote(midiout,chan,conv_note,vol)

    beat += 1
    loop += 1
    
    if loop < (tsig * 4):
        threading.Timer(speed/timing,play_bass,[midiout, chan, speed, vol, beat, loop, pattern]).start()

def play_drums(midiout, chan, speed, vol, beat, loop, pattern):
    beatarray = [list(pattern[0][1:]),list(pattern[1][1:]),list(pattern[2][1:])]

    # HATS
    if beatarray[0][(beat % (tsig*timing)) - 1] == "x":
        playnote(midiout,chan,42,vol)

    # SNARE
    if beatarray[1][(beat % (tsig*timing)) - 1] == "x":
        playnote(midiout,chan,40,vol)

    # KICK
    if beatarray[2][(beat % (tsig*timing)) - 1] == "x":
        playnote(midiout,chan,36,vol)

    beat += 1
    loop += 1

    if loop < (tsig * 4):
        threading.Timer(speed/timing, play_drums, [midiout, chan, speed, vol, beat, loop, pattern]).start()

def enqueue_drums(midiout, tempo):
    while len(drumlines) > 0:
        play_drums(midiout, 0x90, tempo, 100, beat, 0, drumlines[0].split())
        time.sleep(tempo*tsig)
        drumlines.pop(0)

def enqueue_bass(midiout, tempo):
    while len(basslines) > 0:
        play_bass(midiout, 0x91, tempo, 127, beat, 0, basslines[0].split())
        time.sleep(tempo*tsig)
        basslines.pop(0)

def add_bass(pattern):
    basslines.append(pattern)

def add_drums(pattern):
    drumlines.append(pattern)

def main():
    midiout = rtmidi.MidiOut(1)
    available_ports = midiout.get_ports()
    print available_ports

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

if __name__ == '__main__':
    main()

