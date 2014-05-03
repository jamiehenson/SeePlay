from abjad import *
from PySide import QtGui
import tools
import watchman
import performer
import conductor

show_piano_righthand = True
show_piano_lefthand = True
show_bass = True
show_stabs = True

score = Score([])
piano_staff = scoretools.PianoStaff([])
upper_staff = Staff([])
lower_staff = Staff([])
bass_staff = Staff([])
stabs_staff = Staff([])

bass_count = 0
melody_count = 0
chords_count = 0

melody = instrumenttools.Piano(
    instrument_name="Melody",
    short_instrument_name="M."
)
chords = instrumenttools.Piano(
    instrument_name="Lead",
    short_instrument_name="L."
)
stabs = instrumenttools.Piano(
    instrument_name="Stabs",
    short_instrument_name="S."
)
bass = instrumenttools.BassTrombone(
    instrument_name='Bass',
    short_instrument_name='B.',
    allowable_clefs=['bass'],
    pitch_range='[E0, E4]',
)

def lily_length(leng):
    if leng == "r1":
        return leng

    lenconv = {
        "se" : "16",
        "qu" : "8",
        "dq" : "8.",
        "cr" : "4",
        "dc" : "4.",
        "mi" : "2",
        "dm" : "2.",
        "S1" : "1",
        "S2" : "1",
        "S3" : "1",
        "S4" : "1",
        "S6" : "1",
        "S8" : "1"
    }
    return str(lenconv[leng])

def lily_note(note):
    note = list(note)
    if len(note) == 2:
        note[1] = "s" if note[1] == "#" else "f"

    return "".join(note).lower()

def lily_octave(oct, instmid):
    octstr = ""
    octdiff = int(oct) - instmid

    if octdiff > 0:
        for i in xrange(octdiff):
            octstr += "\'"
    elif octdiff < 0:
        for i in xrange(abs(octdiff)):
            octstr += ","

    return octstr

def lily_convert_chord(bar):
    sequence = list(bar)
    lilybar = []

    for chord in sequence:
        if chord != ".":
            length = lily_length(str(chord[-2:]))
            if chord.startswith("r") == False:
                chordnotes = tools.get_chord(chord)
                chordsize = 3
                octave = lily_octave(int(chord[-4:-3]), 2)

                lilychord = "<"
                for i in xrange(chordsize):
                    note = chordnotes[i]
                    pitch = tools.midi_to_genletter(note)
                    
                    lilynote = str(lily_note(pitch) + octave + " ")
                    lilychord += lilynote
                lilychord += ">" + length
                lilybar.append(lilychord)
            elif chord == "r1":
                lilybar.append(chord + " ")
            else:
                lilybar.append("r" + length + " ")

    return " ".join(lilybar)

def lily_convert_single(bar):
    sequence = list(bar)
    lilybar = []

    for note in sequence:
        if note != ".":
            length = lily_length(str(note[-2:]))
            if note.startswith("r") == False:
                if len(note) == 5:
                    pitch = note[:2]
                else:
                    pitch = note[:1]

                octave = lily_octave(int(note[-3:-2]), 1)
                lilynote = str(lily_note(pitch) + octave + length + " ")

                lilybar.append(lilynote)
            elif note == "r1":
                lilybar.append(note + " ")
            else:
                lilybar.append("r" + length + " ")

    # print "Bar test:", str(sequence) + " | " + str(lilybar)

    return " ".join(lilybar)

def change_tsig():
    global bass_staff
    tsig = indicatortools.TimeSignature((4, 4))
    attach(tsig, bass_staff)

def add_melody_bar(bar):
    global upper_staff, melody_count

    if watchman.active == True and len(performer.melodylines) > 0:
        bar = lily_convert_single(bar)
        upper_staff.extend(bar)
        melody_count += 1

def add_chords_bar(bar):
    global lower_staff, chords_count
    
    if watchman.active == True and len(performer.chordlines) > 0:
        bar = lily_convert_chord(bar)
        lower_staff.extend(bar)
        chords_count += 1

def add_bass_bar(bar):
    global bass_staff, bass_count

    if watchman.active == True and len(performer.basslines) > 0:
        bar = lily_convert_single(bar)
        bass_staff.extend(bar)
        bass_count += 1

def init():
    global piano_staff, bass_staff, score, lower_staff, upper_staff

    score = Score([])
    piano_staff = scoretools.PianoStaff([])
    upper_staff = Staff([])
    lower_staff = Staff([])
    bass_staff = Staff([])

    attach(Clef('bass'), lower_staff)
    attach(melody, upper_staff)
    attach(chords, lower_staff)

    attach(Clef('bass'), bass_staff)
    attach(bass, bass_staff)

def topup():
    global bass_count, melody_count, chords_count

    complen = max([bass_count, chords_count, melody_count])
    
    while bass_count < complen:
        bass_staff.extend("r1")
        bass_count += 1

    while melody_count < complen:
        melody_staff.extend("r1")
        melody_count += 1

    while chords_count < complen:
        chords_staff.extend("r1")
        chords_count += 1

def form_key():
    key = conductor.relativekey
    mode = conductor.relativemode

    if mode in ["ionian", "lydian", "mixolydian", "major"]:
        mode = "major" 
    else:
        mode = "minor"

    keyz = ["A major",
            "A minor",
            "Ab major",
            "Ab minor",
            "A# minor",
            "B major",
            "B minor",
            "Bb major",
            "Bb minor",
            "C major",
            "C minor",
            "Cb major",
            "C# major",
            "C# minor",
            "D major",
            "D minor",
            "Db major",
            "D# minor",
            "E major",
            "E minor",
            "Eb major",
            "Eb minor",
            "F major",
            "F minor",
            "F# major",
            "F# minor",
            "G major",
            "G minor",
            "Gb major",
            "G# minor"]

    if str(key + " " + mode) in keyz:
        keylist = list(key)

        if len(keylist) == 2:
            if keylist[1] == "b":
                keylist[1] = "f"
            elif keylist[1] == "#":
                keylist[1] = "s"

        key = "".join(keylist)
        key = key.lower()
    else:
        key = "c"
        mode = "major"

    return str(key), str(mode)

def make(parent):
    global piano_staff, bass_staff

    topup()

    key, mode = form_key()

    key_signature = KeySignature(key, mode)
    attach(key_signature, upper_staff)
    attach(key_signature, lower_staff)
    attach(key_signature, bass_staff)

    if (show_piano_righthand): piano_staff.append(upper_staff)
    if (show_piano_lefthand): piano_staff.append(lower_staff)
    if (show_piano_righthand or show_piano_lefthand): score.append(piano_staff)
    if (show_bass): score.append(bass_staff)

    print "Compiling sheet music..."

    lily = lilypondfiletools.make_basic_lilypond_file(score)

    lily.header_block.title = markuptools.Markup(parent.user_score_title)
    lily.header_block.composer = markuptools.Markup('SeePlay')
    lily.global_staff_size = 16
    # lily.default_paper_size = 'A4', 'portrait'
    show(lily)

    bass_count = 0
    melody_count = 0
    chords_count = 0

    print "Sheet music compiled."
