from abjad import *
import general_composer

score = Score([])
piano_staff = scoretools.PianoStaff([])
upper_staff = Staff([])
lower_staff = Staff([])
bass_staff = Staff([])

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

def lily_octave(oct):
    octstr = ""
    octdiff = int(oct) - 4

    if octdiff > 0:
        for i in xrange(octdiff):
            octstr += "\'"
    elif octdiff < 0:
        for i in xrange(octdiff):
            octstr += ","
    
    return octstr

def lily_convert_chord(bar):
    print bar
    sequence = list(bar)
    lilybar = []

    for chord in sequence:
        if chord != ".":
            chordnotes = general_composer.get_chord(chord)
            length = chord[-2:]
            chordsize = 6

            if len(chord) == 6:
                pitch = note[:2]
            else:
                pitch = note[:1]


            octave = lily_octave(int(chord[-4:-3]))
            length = lily_length(str(chord[-2:]))
            lilynote = str(pitch.lower() + length + octave + " ")
            lilybar.append(lilynote)

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
            lilynote = str(pitch.lower() + length + octave + " ")
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
    lower_staff.extend(bar)

def add_bass_bar(bar):
    global bass_staff
    bar = lily_convert_bass(bar)
    bass_staff.extend(bar)

piano = instrumenttools.Piano()
bass = instrumenttools.BassTrombone(
    instrument_name='Bass',
    short_instrument_name='B.',
    allowable_clefs=['bass'],
    pitch_range='[E0, E4]',
)

def init_score():
    global piano_staff, bass_staff
    attach(Clef('bass'), lower_staff)
    attach(piano, piano_staff)

    attach(Clef('bass'), bass_staff)
    attach(bass, bass_staff)

def write():
    init_score()

    add_chords_bar("e'4 d'4 e'4 f'4")
    add_bass_bar("c'2. b8 a8")
    add_bass_bar("c'2. b8 d8")

    #change_tsig()

    make()

def make():
    global piano_staff, bass_staff
    piano_staff.append(upper_staff)
    piano_staff.append(lower_staff)
    score.append(piano_staff)
    score.append(bass_staff)

    lily = lilypondfiletools.make_basic_lilypond_file(score)
    lily.header_block.title = markuptools.Markup('SeePlay Demo')
    lily.header_block.composer = markuptools.Markup('Jamie Henson')
    lily.global_staff_size = 16
    lily.default_paper_size = 'A4', 'portrait'
    show(lily)

if __name__ == "__main__":
    write()
