import general_composer
import performer
import conductor
import random

current_melody = ". . . . . . . . . . . . . . . ."

def make_phrase(template, scale):
    bar = []
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + str(note[-2:]))
        bar.append(note)
    return " ".join(bar)

def gen_rhythm(template, threshold):
    # Rhythm
    for i in xrange(int(performer.tsig * performer.timing)):
        if random.random() < (0.2 * (threshold + 1)):
            template.append("x")
        else:
            template.append(".")

    return template

def gen_notes(template):
    # Note lengths and pitch
    if "x" in template:
        for i in xrange(int(performer.tsig * performer.timing)):
            if template[i] != ".":
                template = general_composer.place_notes(i, template, True)
    else:
        template[0] = "r1"

    # Starting rest
    if template[0] == '.':
        template = general_composer.place_notes(0, template, False)

    return template

def gen(threshold):
    global current_melody

    template = []
    template = gen_rhythm(template, threshold)
    template = gen_notes(template)

    current_melody = " ".join(template)

# Ambient
def ambient(parent, threshold):
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(3)

    scale = general_composer.make_scale(key, mode, octave)
    bar = make_phrase(current_melody, scale)

    while len(performer.melodylines) <= performer.buff:
        performer.add_melody(bar)
