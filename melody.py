import tools
import performer
import conductor
import random
import section
import watchman

current_melody = ". . . . . . . . . . . . . . . ."
rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
m_lock = False
prev_degree = 0
degree = 0

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
    global degree, prev_degree
    # Note lengths and pitch
    newtem = template
    edited = False
    newdeg = 0

    for i in xrange(int(performer.tsig * performer.timing)):
        if template[i] != ".":
            newdeg, newtem = tools.place_notes(i, template, True, degree, prev_degree)
            prev_degree = degree
            degree = newdeg
            edited = True
    
    if edited == False:
        newtem[0] = "r1"

    # Starting rest
    if template[0] == '.':
        newdeg, newtem = tools.place_notes(0, template, False, degree, prev_degree)

    return newtem

def gen():
    global current_melody, m_lock
    if m_lock == False:
        current_melody = " ".join(gen_notes(gen_rhythm(rhythm)))
        m_lock = True

def play():
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(3)

    scale = tools.make_scale(key, mode, octave)
    bar = make_phrase(current_melody, scale)

    while len(performer.melodylines) <= performer.buff:
        performer.add_melody(bar)
