import tools
import performer
import conductor
import random
import section
import watchman

current_bass = ". . . . . . . . . . . . . . . ."
rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
b_lock = False
degree = 0 # The tonic by default

def make_phrase(template, scale):
    bar = ""
    sequence = template.split()
    for note in sequence:
        if note != "." and note.startswith("r") == False:
            note = str(scale[int(note[:1])] + str(note[-2:]))
        bar += (note + " ")
    return bar

def gen_rhythm(template):
    newtem = template
    for i in xrange(len(template)):
        if (random.random() < watchman.activities["bass"]):
            if template[i] == ".":
                newtem[i] = "x"
            else:
                newtem[i] = "."

    return newtem

def gen_notes(template):
    global degree
    # Note lengths and pitch
    newtem = template
    edited = False

    # print "B", newtem
    for i in xrange(int(performer.tsig * performer.timing)):
        if template[i] != ".":
            # print "Before", degree
            degree, newtem = tools.place_notes(i, template, True, degree)
            edited = True
            # print "After", degree
    # print "A", newtem

    degree = 0

    if edited == False:
        newtem[0] = "r1"

    # Starting rest
    if template[0] == '.':
        degree, newtem = tools.place_notes(0, template, False, degree)

    return newtem

def gen():
    global current_bass, b_lock
    if b_lock == False:
        current_bass = " ".join(gen_notes(gen_rhythm(rhythm)))
        b_lock = True

def play():
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(1)

    scale = tools.make_scale(key, mode, octave)

    bar = make_phrase(current_bass, scale)

    while len(performer.basslines) <= performer.buff: 
        performer.add_bass(bar)
