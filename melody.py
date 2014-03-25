import tools
import performer
import conductor
import random
import section
import watchman

current_melody = ". . . . . . . . . . . . . . . ."

def make_phrase(template, scale):
    bar = []
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + str(note[-2:]))
        bar.append(note)
    return " ".join(bar)

def gen_rhythm(template):
    newtem = template
    for i in xrange(len(template)):
        if (random.random() < watchman.activities["melody"]):
            if template[i] == ".":
                newtem[i] = "x"
            else:
                newtem[i] = "."

    return newtem

def gen_notes(template):
    # Note lengths and pitch
    newtem = template
    if "x" in template:
        for i in xrange(int(performer.tsig * performer.timing)):
            if template[i] != ".":
                newtem = tools.place_notes(i, template, True)
    else:
        newtem[0] = "r1"

    # Starting rest
    if template[0] == '.':
        newtem = tools.place_notes(0, template, False)

    return newtem

def gen():
    global current_melody

    template = section.rhythm
    template = gen_rhythm(template)
    template = gen_notes(template)

    current_melody = " ".join(template)

def play():
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(3)

    scale = tools.make_scale(key, mode, octave)
    bar = make_phrase(current_melody, scale)

    while len(performer.melodylines) <= performer.buff:
        performer.add_melody(bar)
