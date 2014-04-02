import tools
import performer
import conductor
import random
import watchman
import section
import bass

current_chords = ". . . . . . . . . . . . . . . ."
rhythm = [".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."]
c_lock = False
prev_degree = 0
degree = 0

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
        if (random.random() < float(watchman.activities["chords"])):
            if template[i] == "." and newtem.count("x") <= section.xlim:
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

    # print "A", newtem
    for i in xrange(int(performer.tsig * performer.timing)):
        if template[i] == "x":
            newdeg, newtem = tools.place_notes(i, template, True, degree, prev_degree)
            prev_degree = degree
            degree = newdeg
            edited = True
        else:
            newtem[i] = "."
    # print "B", newtem

    if edited == False:
        newtem[0] = "r1"

    # Starting rest
    if template[0] == '.':
        newdeg, newtem = tools.place_notes(0, template, False, degree, prev_degree)

    return newtem

def gen():
    global current_chords, c_lock
    if c_lock == False: 
        current_chords = " ".join(gen_notes(gen_rhythm(rhythm)))
        c_lock = True

def play():
    global current_chords
    key = conductor.relativekey
    mode = conductor.relativemode
    octave = str(2)

    scale = tools.make_chordscale(key, mode, octave)
    bar = make_phrase(current_chords, scale)

    while len(performer.chordlines) <= performer.buff:
        performer.add_chords(bar)
