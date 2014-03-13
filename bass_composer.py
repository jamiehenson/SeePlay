import general_composer
import performer
import conductor
import random
import watchman

current_bass = ". . . . . . . . . . . . . . . ."

def make_phrase(template, scale):
    bar = ""
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + str(note[-2:]))
        bar += (note + " ")

    return bar

def gen_rhythm(template):
    # Rhythm
    # print performer.tsig, performer.timing
    for i in xrange(int(performer.tsig * performer.timing)):
        if random.random() < watchman.activities["bass"]:
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

def gen():
    global current_bass

    template = []
    template = gen_rhythm(template)
    template = gen_notes(template)

    current_bass = " ".join(template)

# Ambient
def ambient():
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(1)

    scale = general_composer.make_scale(key, mode, octave)

    bar = make_phrase(current_bass, scale)
    while len(performer.basslines) <= performer.buff: 
        performer.add_bass(bar)
