import general_composer
import performer
import conductor

def make_phrase(template, scale):
    thisbar = ""

    sequence = template.split()
    for note in sequence:
        if note != ".":
            note = str(scale[int(note[:1])] + note[-2:])
        thisbar += (note + " ")

    return thisbar

def gen(inst):
    return 0

# Ambient
def ambient(parent, threshold):
    key = conductor.relativekey
    mode = conductor.relativemode
    thisbar = ""
    octave = str(2)

    chordscale = general_composer.make_chordscale(key, mode, octave)

    template1 = "0S1 . . . . . . . . . . . . . . ."
    template2 = "0cr . . . . . . . 1mi . . . . . ."
    template3 = "0cr . . 1cr . . 4cr . . . 0cr . 0cr . . ."

    if threshold == 0:
        thisbar = make_phrase(template1, chordscale)
    elif threshold == 1:
        thisbar = make_phrase(template2, chordscale)
    elif threshold == 2:
        thisbar = make_phrase(template3, chordscale)

    thisbar += "."

    while len(performer.chords) <= performer.buff: 
        performer.add_chords(thisbar)
