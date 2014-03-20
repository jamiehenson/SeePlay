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
    newtem = []
    for note in template:
        if (random.random() < watchman.activities["melody"]):
            if note == ".":
                newtem.append("x")
            else:
                newtem.append(".")
        else:
            newtem.append(note)

    return newtem

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
