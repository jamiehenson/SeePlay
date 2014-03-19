import tools
import performer
import conductor
import random
import watchman
import bass

current_chords = ". . . . . . . . . . . . . . . ."

def make_phrase(template, scale):
    bar = []
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + note[-2:])
        bar.append(note)
    return " ".join(bar)

def gen_rhythm(template):
    # Rhythm
    # Borrow rhythm from the bass
    template = []

    # bassbar = bass.current_bass
    # bb_list = bassbar.split(" ")
    # for note in bb_list:
    for i in xrange(int(performer.tsig * performer.timing)):    
        if random.random() < watchman.activities["chords"]:
            template.append("x")
        else:
            template.append(".")

    return template

def gen_notes(template):
    # Note lengths and pitch
    if "x" in template:
        for i in xrange(int(performer.tsig * performer.timing)):
            if template[i] != ".":
                template = tools.place_notes(i, template, True)
    else:
        template[0] = "r1"

    # Starting rest
    if template[0] == '.':
        template = tools.place_notes(0, template, False)

    return template

def gen():
    global current_chords

    template = []
    template = gen_rhythm(template)
    template = gen_notes(template)

    current_chords = " ".join(template)

def play():
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(2)

    scale = tools.make_chordscale(key, mode, octave)
    bar = make_phrase(current_chords, scale)

    while len(performer.chords) <= performer.buff:
        performer.add_chords(bar)

