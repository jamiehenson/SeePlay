from abjad import *
import general_composer

show_piano_righthand = True
show_piano_lefthand = False
show_bass = True

score = Score([])
piano_staff = scoretools.PianoStaff([])
upper_staff = Staff([])
lower_staff = Staff([])
bass_staff = Staff([])

piano = instrumenttools.Piano()
bass = instrumenttools.BassTrombone(
    instrument_name='Bass',
    short_instrument_name='B.',
    allowable_clefs=['bass'],
    pitch_range='[E0, E4]',
)

def lily_length(leng):
    lenconv = {
        "se" : 16,
        "qu" : 8,
        "cr" : 4,
        "mi" : 2,
        "S1" : 1,
        "S2" : 1,
        "S3" : 1,
        "S4" : 1,
        "S6" : 1,
        "S8" : 1
    }
    return str(lenconv[leng])

def lily_note(note):
    note = list(note)
    if len(note) == 2:
        note[1] = "s" if note[1] == "#" else "f"

    return "".join(note).lower()

def lily_octave(oct):
    octstr = ""
    octdiff = int(oct) - 2

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
            chordnotes = general_composer.get_chord(chord)
            chordsize = 3
            octave = lily_octave(int(chord[-4:-3]))
            length = lily_length(str(chord[-2:]))

            lilychord = "<"
            for i in xrange(chordsize):
                note = chordnotes[i]
                pitch = general_composer.midi_to_genletter(note)
                
                lilynote = str(lily_note(pitch) + octave + " ")
                lilychord += lilynote
            lilychord += ">" + length
            lilybar.append(lilychord)

    return lilybar

def lily_convert_bass(bar):
    sequence = list(bar)
    lilybar = []

    for note in sequence:
        if note != ".":
            if len(note) == 5:
                pitch = note[:2]
            else:
                pitch = note[:1]

            octave = lily_octave(int(note[-3:-2]))
            length = lily_length(str(note[-2:]))
            lilynote = str(lily_note(pitch) + octave + length + " ")
            lilybar.append(lilynote)

    return lilybar

def change_tsig():
    global bass_staff
    tsig = indicatortools.TimeSignature((4, 4))
    attach(tsig, bass_staff)

def add_chords_bar(bar):
    global upper_staff, lower_staff
    bar = lily_convert_chord(bar)
    upper_staff.extend(bar)
    #lower_staff.extend(bar)

def add_bass_bar(bar):
    global bass_staff
    bar = lily_convert_bass(bar)
    bass_staff.extend(bar)

def init_score():
    global piano_staff, bass_staff
    attach(Clef('bass'), lower_staff)
    attach(piano, piano_staff)

    attach(Clef('bass'), bass_staff)
    attach(bass, bass_staff)

def make():
    global piano_staff, bass_staff
    if (show_piano_righthand): piano_staff.append(upper_staff)
    if (show_piano_lefthand): piano_staff.append(lower_staff)
    if (show_piano_righthand or show_piano_lefthand): score.append(piano_staff)
    if (show_bass): score.append(bass_staff)

    print "Compiling sheet music..."

    lily = lilypondfiletools.make_basic_lilypond_file(score)
    lily.header_block.title = markuptools.Markup('SeePlay Demo')
    lily.header_block.composer = markuptools.Markup('Jamie Henson')
    lily.global_staff_size = 16
    lily.default_paper_size = 'A4', 'portrait'
    show(lily)
