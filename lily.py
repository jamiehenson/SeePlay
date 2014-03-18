from abjad import *
from PySide import QtGui
import tools

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

melody = instrumenttools.Piano(
    instrument_name="Melody",
    short_instrument_name="M."
)
chords = instrumenttools.Piano(
    instrument_name="Lead",
    short_instrument_name="C."
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
        if chord == 'r1':
            lilybar.append("r1")
            break

        if chord != ".":
            chordnotes = tools.get_chord(chord)
            chordsize = 3
            octave = lily_octave(int(chord[-4:-3]), 2)
            length = lily_length(str(chord[-2:]))

            lilychord = "<"
            for i in xrange(chordsize):
                note = chordnotes[i]
                pitch = tools.midi_to_genletter(note)
                
                lilynote = str(lily_note(pitch) + octave + " ")
                lilychord += lilynote
            lilychord += ">" + length
            lilybar.append(lilychord)

    return " ".join(lilybar)

def lily_convert_single(bar):
    sequence = list(bar)
    lilybar = []

    for note in sequence:
        if note == 'r1':
            lilybar.append("r1")
            break
        
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
            else:
                lilybar.append("r" + length)

    return " ".join(lilybar)

def change_tsig():
    global bass_staff
    tsig = indicatortools.TimeSignature((4, 4))
    attach(tsig, bass_staff)

def add_melody_bar(bar):
    global upper_staff
    bar = lily_convert_single(bar)
    upper_staff.extend(bar)

def add_chords_bar(bar):
    global lower_staff
    bar = lily_convert_chord(bar)
    lower_staff.extend(bar)

def add_bass_bar(bar):
    global bass_staff
    bar = lily_convert_single(bar)
    bass_staff.extend(bar)

def init():
    global piano_staff, bass_staff
    attach(Clef('bass'), lower_staff)
    attach(melody, upper_staff)
    attach(chords, lower_staff)

    attach(Clef('bass'), bass_staff)
    attach(bass, bass_staff)

def make(parent):
    global piano_staff, bass_staff
    if (show_piano_righthand): piano_staff.append(upper_staff)
    if (show_piano_lefthand): piano_staff.append(lower_staff)
    if (show_piano_righthand or show_piano_lefthand): score.append(piano_staff)
    if (show_bass): score.append(bass_staff)

    print "Compiling sheet music..."

    lily = lilypondfiletools.make_basic_lilypond_file(score)
    lily.header_block.title = markuptools.Markup(parent.user_score_title)
    lily.header_block.composer = markuptools.Markup('SeePlay')
    lily.global_staff_size = 16
    lily.default_paper_size = 'A4', 'portrait'
    show(lily)
