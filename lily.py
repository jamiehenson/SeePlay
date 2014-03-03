from abjad import *

score = Score([])
piano_staff = scoretools.PianoStaff([])
upper_staff = Staff([])
lower_staff = Staff([])
bass_staff = Staff([])

def change_tsig():
    global bass_staff
    tsig = indicatortools.TimeSignature((4, 4))
    attach(tsig, bass_staff)

def add_chords_bar(bar):
    global upper_staff, lower_staff
    upper_staff.extend(bar)
    lower_staff.extend(bar)

def add_bass_bar(bar):
    global bass_staff
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

    lily_make()

def lily_make():
    global piano_staff, bass_staff
    piano_staff.append(upper_staff)
    piano_staff.append(lower_staff)
    score.append(piano_staff)
    score.append(bass_staff)

    lily = lilypondfiletools.make_basic_lilypond_file(score)
    lily.header_block.title = markuptools.Markup('SeePlay Demo')
    lily.header_block.composer = markuptools.Markup('Sen')
    lily.global_staff_size = 16
    lily.default_paper_size = 'A4', 'portrait'
    show(lily)

if __name__ == "__main__":
    write()
