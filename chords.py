import tools
import performer
import conductor
import random
import watchman
import section
import bass

current_chords = ". . . . . . . . . . . . . . . ."
rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]

def make_phrase(template, scale):
    bar = []
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + note[-2:])
        bar.append(note)
    return " ".join(bar)

def gen_rhythm(template):
    newtem = template
    for i in xrange(len(template)):
        if (random.random() < watchman.activities["chords"]):
            if template[i] == ".":
                newtem[i] = "x"
            else:
                newtem[i] = "."

    return newtem

def gen_notes(template):
    # Note lengths and pitch
    newtem = template
    edited = False

    for i in xrange(int(performer.tsig * performer.timing)):
        if template[i] != ".":
            newtem = tools.place_notes(i, template, True)
            edited = True
    
    if edited == False:
        newtem[0] = "r1"

    # Starting rest
    if template[0] == '.':
        newtem = tools.place_notes(0, template, False)

    return newtem

def gen():
    global current_chords
    template = rhythm
    template = gen_rhythm(template)
    template = gen_notes(template)
    current_chords = " ".join(template)

def play():
    global current_chords
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(2)

    scale = tools.make_chordscale(key, mode, octave)
    bar = make_phrase(current_chords, scale)

    while len(performer.chords) <= performer.buff:
        performer.add_chords(bar)

